from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.tutor_register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('switch-role/<str:role>/', views.switch_role, name='switch_role'),
    path('dashboard/tutor/', views.tutor_dashboard, name='tutor_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),


    # Tutor course management
    path('upload-course/', views.upload_course, name='upload_course'),
    path('manage-course/', views.manage_course, name='manage_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),

    # Student course access
    path("available-courses/", views.available_courses, name="available_courses"),
    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),

    # Resources
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('courses/<int:course_id>/details/', views.course_detail, name='course_detail'),

    # Tutor profile
    path('dashboard/tutor/profile/', views.tutor_profile, name='tutor_profile'),
   
    #Q&A
    path('courses/<int:course_id>/questions/', views.course_questions, name='course_questions'),
    path('questions/<int:question_id>/answer/', views.add_answer, name='add_answer'),

]
