from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import FacultyProfile, Course

@login_required
def dashboard(request):
    try:
        profile = FacultyProfile.objects.get(user=request.user)
        courses = Course.objects.filter(faculty=profile)
        
        context = {
            'profile': profile,
            'courses': courses,
        }
        return render(request, 'faculty/dashboard.html', context)
    except FacultyProfile.DoesNotExist:
        # Redirect to profile creation if profile doesn't exist
        return redirect('faculty:create_profile')

# Add more views for different dashboard functionalities
