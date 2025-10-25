from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import TutorRegisterForm, TutorProfileForm, CourseForm, ResourceForm
from .models import CustomUser, TutorProfile, Course, Enrollment, Resource,Question, Answer

User = get_user_model()

# ------------------------------
# Home View
# ------------------------------
def home(request):
    return render(request, 'main/home.html')

# ------------------------------
# User Login
# ------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        # Authenticate existing user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # ✅ always go to dashboard

        # Auto-create student if user doesn't exist
        if not CustomUser.objects.filter(username=username).exists():
            new_user = CustomUser.objects.create_user(
                username=username,
                password=password,
                is_student=True,
                is_tutor=False
            )
            login(request, new_user)
            messages.success(request, f"Welcome {username}! A student account has been created.")
            return redirect('dashboard')  # ✅ fixed

        messages.error(request, "Invalid username or password")

    return render(request, 'main/login.html')


# ------------------------------
# User Logout
# ------------------------------
def user_logout(request):
    logout(request)
    return redirect('home')

# ------------------------------
# Tutor Registration
# ------------------------------

def tutor_register(request):
    # Logged-in user upgrading to tutor
    if request.user.is_authenticated:
        user = request.user
        profile_form = TutorProfileForm(request.POST or None)
        if request.method == 'POST' and profile_form.is_valid():
            user.is_tutor = True
            user.is_student = True  # Keep student role
            user.current_role = 'tutor'
            user.save()

            TutorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'contact_info': profile_form.cleaned_data['contact_info'],
                    'phone_number': profile_form.cleaned_data['phone_number'],
                    'department': profile_form.cleaned_data['department']
                }
            )

            messages.success(request, "You are now registered as a tutor!")
            return redirect('dashboard')

        return render(request, 'main/register.html', {
            'profile_form': profile_form,
            'user_form': None
        })

    # New user registering as tutor
    else:
        user_form = TutorRegisterForm(request.POST or None)
        profile_form = TutorProfileForm(request.POST or None)

        if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            email = user_form.cleaned_data['email']

            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            # Always update role flags
            user.is_tutor = True
            user.is_student = True
            user.current_role = 'tutor'
            if password:
                user.set_password(password)
            user.save()

            TutorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'contact_info': profile_form.cleaned_data['contact_info'],
                    'phone_number': profile_form.cleaned_data['phone_number'],
                    'department': profile_form.cleaned_data['department']
                }
            )

            login(request, user)
            messages.success(request, "You are now registered as a tutor!")
            return redirect('dashboard')

        return render(request, 'main/register.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
   
         

         
# ------------------------------
# Dashboard
# ------------------------------
@login_required
def dashboard(request):
    user = request.user

    # Both roles: check session role
    if user.is_student and user.is_tutor:
        current_role = request.session.get('current_role', 'student')  # default = student
        return render(request, 'main/dashboard_role_switch.html', {'current_role': current_role})

    elif user.is_tutor:
        return redirect('tutor_dashboard')

    else:
        return redirect('student_dashboard')


def switch_role(request, role):
    user = request.user
    if role == 'student' and user.is_student:
        request.session['current_role'] = 'student'
        messages.success(request, "Switched to Student View")
        return redirect('dashboard')

    elif role == 'tutor' and user.is_tutor:
        request.session['current_role'] = 'tutor'
        messages.success(request, "Switched to Tutor View")
        return redirect('tutor_dashboard')

    else:
        messages.error(request, "You do not have permission for this role")
        return redirect('dashboard')


# ------------------------------
# Tutor: Upload Course
# ------------------------------
@login_required
def upload_course(request):
    if not request.user.is_tutor:
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = request.user
            course.save()
            messages.success(request, "Course uploaded successfully!")
            return redirect('manage_course')
    else:
        form = CourseForm()

    return render(request, 'tutor/upload_course.html', {'form': form})

# ------------------------------
# Tutor: Manage Courses
# ------------------------------
@login_required
def manage_course(request):
    if not request.user.is_tutor:
        return redirect('login')
    courses = Course.objects.filter(tutor=request.user)
    return render(request, 'tutor/manage_course.html', {'courses': courses})

# ------------------------------
# Tutor: Edit Course
# ------------------------------
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, tutor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('manage_course')
    else:
        form = CourseForm(instance=course)
    return render(request, 'tutor/edit_course.html', {'form': form})

# ------------------------------
# Tutor: Delete Course
# ------------------------------
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, tutor=request.user)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('manage_course')

# ------------------------------
# Student: Available Courses
# ------------------------------
@login_required
def available_courses(request):
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(student=request.user).values_list("course_id", flat=True)

    for course in courses:
        course.is_enrolled = course.id in enrolled_courses

    return render(request, "student/available_courses.html", {"courses": courses})

# ------------------------------
# Student: Enroll Course
# ------------------------------
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f"Enrolled in {course.title} successfully!")
    return redirect("available_courses")

# ------------------------------
# Tutor: Add Resource
# ------------------------------
@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.owner = request.user
            resource.save()
            messages.success(request, "Resource added successfully!")
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resources/add_resource.html', {'form': form})

# ------------------------------
# List Resources
# ------------------------------
@login_required
def resource_list(request):
    query = request.GET.get('q')
    if query:
        resources = Resource.objects.filter(title__icontains=query)
    else:
        resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'resources/resource_list.html', {'resources': resources})

# ------------------------------
# Resource Details
# ------------------------------
@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})

# ------------------------------
# Tutor Profile View
# ------------------------------
@login_required
def tutor_profile(request):
    return render(request, 'tutor/profile.html')
# ------------------------------
# Switch Role View
def switch_role(request, role):
    user = request.user
    if role == 'student' and user.is_student:
        user.current_role = 'student'
        user.save()
        messages.success(request, "Switched to Student View")
        return redirect('dashboard')

    elif role == 'tutor' and user.is_tutor:
        user.current_role = 'tutor'
        user.save()
        messages.success(request, "Switched to Tutor View")
        return redirect('tutor_dashboard')

    else:
        messages.error(request, "You do not have permission for this role")
        return redirect('dashboard')
# ------------------------------
# tutor Dashboard
@login_required
def tutor_dashboard(request):
    try:
        tutor = request.user.tutor_profile
    except TutorProfile.DoesNotExist:
        return redirect('student_dashboard')  # or any page you want non-tutors to go

    courses = Course.objects.filter(tutor=request.user)
    recent_materials = Resource.objects.filter(owner=request.user).order_by('-created_at')[:6]

    return render(request, 'tutor/profile.html', {
        'tutor': tutor,
        'courses': courses,
        'recent_materials': recent_materials,
    })


# ------------------------------
# Student Dashboard
@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')
@login_required
def course_questions(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all()

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Question.objects.create(course=course, asked_by=request.user, content=content)
            return redirect('course_questions', course_id=course_id)

    return render(request, 'main/course_questions.html', {'course': course, 'questions': questions})
# ------------------------------
#Q&A: Add Answer

@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Answer.objects.create(question=question, answered_by=request.user, content=content)
            return redirect('course_questions', course_id=question.course.id)

    return render(request, 'main/add_answer.html', {'question': question})
# ------------------------------
# Student: Course Detail View
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'student/course_detail.html', {'course': course})
