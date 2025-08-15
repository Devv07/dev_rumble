from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FacultyProfile, Course
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Student, Assignment

@login_required
def faculty_dashboard(request):
    try:
        profile = FacultyProfile.objects.get(user=request.user)
        courses = Course.objects.filter(faculty=profile)
        announcements = [
            {"title": "University Holiday", "time": "2 days ago", "description": "College will be closed on Friday for Founder's Day"},
            {"title": "Faculty Meeting", "time": "5 days ago", "description": "Monthly faculty meeting scheduled for next Wednesday"},
            {"title": "New LMS Features", "time": "1 week ago", "description": "Check out the new gradebook features in our learning management system"},
        ]
        events = [
            {"title": "Faculty Meeting", "time": "10:00 AM"},
            {"title": "CS101 Office Hours", "time": "2:00 PM"},
            {"title": "Department Lunch", "time": "12:30 PM"},
        ]
        context = {
            'profile': profile,
            'courses': courses,
            'announcements': announcements,
            'events': events,
        }
        return render(request, 'faculty/faculty_dashboard.html', context)
    except FacultyProfile.DoesNotExist:
        return redirect('faculty:profile')

@login_required
def profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        FacultyProfile.objects.create(user=request.user, name=name, department=department)
        return redirect('faculty:faculty_dashboard')
    return render(request, 'faculty/profile.html')

@login_required
def student_management(request):
    try:
        profile = FacultyProfile.objects.get(user=request.user)
        courses = Course.objects.filter(faculty=profile)
        students = Student.objects.filter(course__in=courses)
        if request.method == 'POST':
            if 'add' in request.POST:
                name = request.POST.get('name')
                email = request.POST.get('email')
                course_id = request.POST.get('course_id')
                Student.objects.create(name=name, email=email, course_id=course_id)
                messages.success(request, 'Student added successfully.')
                return redirect('faculty:student_management')
            elif 'update' in request.POST:
                student_id = request.POST.get('student_id')
                student = get_object_or_404(Student, id=student_id)
                student.name = request.POST.get('name')
                student.email = request.POST.get('email')
                student.course_id = request.POST.get('course_id')
                student.save()
                messages.success(request, 'Student updated successfully.')
                return redirect('faculty:student_management')
        return render(request, 'faculty/student_management.html', {'students': students, 'courses': courses, 'profile': profile})
    except FacultyProfile.DoesNotExist:
        return redirect('faculty:profile')

@login_required
def submit_assignment(request):
    try:
        profile = FacultyProfile.objects.get(user=request.user)
        courses = Course.objects.filter(faculty=profile)
        assignments = Assignment.objects.filter(course__in=courses)
        if request.method == 'POST':
            if 'add' in request.POST:
                title = request.POST.get('title')
                description = request.POST.get('description')
                due_date = request.POST.get('due_date')
                course_id = request.POST.get('course_id')
                Assignment.objects.create(title=title, description=description, due_date=due_date, course_id=course_id)
                messages.success(request, 'Assignment created successfully.')
                return redirect('faculty:submit_assignment')
            elif 'update' in request.POST:
                assignment_id = request.POST.get('assignment_id')
                assignment = get_object_or_404(Assignment, id=assignment_id)
                assignment.title = request.POST.get('title')
                assignment.description = request.POST.get('description')
                assignment.due_date = request.POST.get('due_date')
                assignment.course_id = request.POST.get('course_id')
                assignment.save()
                messages.success(request, 'Assignment updated successfully.')
                return redirect('faculty:submit_assignment')
        return render(request, 'faculty/submit_assignment.html', {'assignments': assignments, 'courses': courses, 'profile': profile})
    except FacultyProfile.DoesNotExist:
        return redirect('faculty:profile')

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('faculty:student_management')

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    messages.success(request, 'Assignment deleted successfully.')
    return redirect('faculty:submit_assignment')