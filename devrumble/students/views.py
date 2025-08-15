from django.shortcuts import render
from core.models import Course, StudentCourseProgress, Event, Discussion, Resource, Assignment, StudyGroup
from django.utils import timezone

def dashboard(request):
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    user = request.user
    user_name = user.get_full_name() or user.username
    user_initials = ''.join(name[0].upper() for name in user_name.split() if name)[:2]

    ongoing_courses = StudentCourseProgress.objects.filter(student=user).select_related('course')
    upcoming_events = Event.objects.all().order_by('created_at')[:3]
    recent_discussions = Discussion.objects.all().order_by('-created_at')[:2]
    recent_resources = Resource.objects.all().order_by('-created_at')[:3]
    pending_assignments = Assignment.objects.filter(student=user, is_completed=False, due_date__gte=timezone.now()).count()
    active_courses = StudentCourseProgress.objects.filter(student=user).count()
    study_groups = StudyGroup.objects.filter(members=user).count()
    upcoming_deadlines = Assignment.objects.filter(
        student=user,
        is_completed=False,
        due_date__gte=timezone.now(),
        due_date__lte=timezone.now() + timezone.timedelta(days=7)
    ).count()
    new_discussions = Discussion.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=1)).count()

    context = {
        'user_name': user_name,
        'user_initials': user_initials,
        'upcoming_deadlines': upcoming_deadlines,
        'new_discussions': new_discussions,
        'active_courses': active_courses,
        'pending_assignments': pending_assignments,
        'study_groups': study_groups,
        'ongoing_courses': [
            {
                'title': progress.course.title,
                'instructor': progress.course.instructor.get_full_name() or progress.course.instructor.username,
                'progress': progress.progress,
                'icon': progress.course.icon
            } for progress in ongoing_courses
        ],
        'upcoming_events': upcoming_events,
        'recent_discussions': recent_discussions,
        'recent_resources': recent_resources,
    }
    return render(request, 'student/dashboard.html', context)
def dashboard_view(request):
    return render(request, 'student/dashboard.html')