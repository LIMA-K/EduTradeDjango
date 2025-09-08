
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import TutorRegisterForm,TutorProfileForm,CourseForm,ResourceForm
from .models import Course ,Enrollment,Resource
from django.contrib.auth.decorators import login_required
# Create your views here.
# Home view
def home(request):
    return render(request, 'main/home.html')
def login_view(request):
    return render(request, 'main/login.html')
# User login view using Django's built-in AuthenticationForm
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # or wherever you want
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})
    # Logout view
def user_logout(request):
    logout(request)
    return redirect('home')
    #tutor registration view
def tutor_register(request):
    if request.method == 'POST':
        user_form = TutorRegisterForm(request.POST)
        profile_form = TutorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_tutor = True  # Mark as tutor
            user.save()
            
                     # Save the tutor profile and link it to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = TutorRegisterForm()
        profile_form = TutorProfileForm()

    return render(request, 'main/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
  
# Dashboard view
@login_required
def dashboard_view(request):
    user = request.user
    is_tutor = hasattr(user, 'tutorprofile')  # Checks if user has a TutorProfile
    return render(request, 'main/dashboard.html', {
        'user': user,
        'is_tutor': is_tutor
    })
# Course upload view for tutors
@login_required
def upload_course(request):
    if not request.user.is_tutor:
        return redirect('home')  # Or display a permission denied page

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = request.user
            course.save()
            return redirect('manage_course')  # Go to manage page after upload
    else:
        form = CourseForm()

    return render(request, 'tutor/upload_course.html', {'form': form})
# Course management view for tutors
@login_required
def manage_course(request):
    if not request.user.is_tutor:
        return redirect('login')  # Or render a permission denied page

    courses = Course.objects.filter(tutor=request.user)
    return render(request, 'tutor/manage_course.html', {'courses': courses})
    # Edit  course views
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, tutor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('manage_course')
    else:
        form = CourseForm(instance=course)
    return render(request, 'tutor/edit_course.html', {'form': form})
# Delete course view
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, tutor=request.user)
    course.delete()
    return redirect('manage_course')
# View available courses for students
def available_courses(request):
    courses = Course.objects.all()

    enrolled_courses = Enrollment.objects.filter(student=request.user).values_list("course_id", flat=True)

    for course in courses:
        course.is_enrolled = course.id in enrolled_courses

    return render(request, "student/available_courses.html", {"courses": courses})
# Render the courses in a template
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "⚠️ You are already enrolled in this course.")
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f"✅ You have successfully enrolled in {course.title}!")

    return redirect("available_courses")  # go back to the course list
    # Add a new resource
@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.owner = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resources/add_resource.html', {'form': form})

# List all resources
@login_required
def resource_list(request):
    query = request.GET.get('q')
    if query:
        resources = Resource.objects.filter(title__icontains=query)
    else:
        resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'resources/resource_list.html', {'resources': resources})

# View a single resource
@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})
