from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Step 1: Custom User Model with Roles
class CustomUser(AbstractUser):
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)  # All users are considered students by default

    def __str__(self):
        return self.username

# Step 2: Tutor Profile (only for tutors)
DEPARTMENT_CHOICES = [
    ('MCA', 'Master of Computer Applications'),
    ('BCA', 'Bachelor of Computer Applications'),
    ('BTech-IT', 'Bachelor of Technology in Information Technology'),
    ('BeTech-AI', 'Bachelor of Technology in Artificial Intelligence'),
    ('BeTech-CS', 'Bachelor of Technology in Computer Science'),
    ('BBA', 'Bachelor of Business Administration'),
    ('MBA', 'Master of Business Administration'),
    # Add more as needed
]

class TutorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
    contact_info = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - Tutor"
# Step 3: Course Model
class Course(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_tutor': True})
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_link = models.URLField(blank=True, null=True)
    material = models.FileField(upload_to='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Step 4: Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"