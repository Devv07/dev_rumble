from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # <-- add this

# function to redirect root to dashboard
def redirect_to_dashboard(request):
    return redirect('students:dashboard')  # make sure this matches your student app URL name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard),       # <-- root redirects to dashboard
    path('login/', include('core.urls')),  # login URLs from core app
    path('students/', include('students.urls')),  # dashboard URLs from student app
    path('', include('core.urls')),  # <-- added comma here
    path('faculty/', include('faculty.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
