from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   # path('login/', views.login_view, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.tutor_register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload-course/', views.upload_course, name='upload_course'),
    path('manage-course/', views.manage_course, name='manage_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),


]
