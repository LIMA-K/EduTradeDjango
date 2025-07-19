from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   # path('login/', views.login_view, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.tutor_register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
