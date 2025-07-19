
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import TutorRegisterForm,TutorProfileForm



from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'main/home.html')
def login_view(request):
    return render(request, 'main/login.html')

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
  

@login_required
def dashboard_view(request):
    user = request.user
    is_tutor = hasattr(user, 'tutorprofile')  # Checks if user has a TutorProfile
    return render(request, 'main/dashboard.html', {
        'user': user,
        'is_tutor': is_tutor
    })
