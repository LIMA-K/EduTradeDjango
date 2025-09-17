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
    path("available-courses/", views.available_courses, name="available_courses"),
    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('dashboard/tutor/profile/', views.tutor_profile, name='tutor_profile')


]
