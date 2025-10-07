from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Default role to STUDENT if not provided
        if 'role' not in extra_fields or not extra_fields['role']:
            extra_fields['role'] = self.model.Role.STUDENT
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # Ensure admin flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Force ADMIN role for superusers
        extra_fields['role'] = self.model.Role.ADMIN

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return super().create_superuser(username, email=email, password=password, **extra_fields)

class User(AbstractUser):
     class Role(models.TextChoices):
         ADMIN = 'ADMIN', 'Admin'
         STUDENT = 'STUDENT', 'Student'

     role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
     objects = CustomUserManager()
 
     def __str__(self):
         return f"{self.username} ({self.role})"

class Class(models.Model):
     class_name = models.CharField(max_length=100, unique=True)
 
     def __str__(self):
         return self.class_name


class Student(models.Model):
     name = models.CharField(max_length=150)
     roll_no = models.CharField(max_length=50)
     class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

     class Meta:
         unique_together = ('roll_no', 'class_ref')

     def __str__(self):
         return f"{self.name} - {self.class_ref.class_name}"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')

    class Meta:
        unique_together = ('subject_name', 'class_ref')

    def __str__(self):
        return f"{self.subject_name} ({self.class_ref.class_name})"


class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()

    class Meta:
        unique_together = ('exam_name', 'class_ref', 'exam_date')

    def __str__(self):
        return f"{self.exam_name} - {self.class_ref.class_name}"


class Result(models.Model):
    class GradeChoices(models.TextChoices):
        PASS = 'Pass', 'Pass'
        FAIL = 'Fail', 'Fail'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade = models.CharField(max_length=10, choices=GradeChoices.choices, blank=True)

    class Meta:
        unique_together = ('student', 'exam', 'subject')

    def save(self, *args, **kwargs):
        try:
            marks_float = float(self.marks)
        except (TypeError, ValueError):
            marks_float = 0.0
        self.grade = self.GradeChoices.PASS if marks_float >= 40 else self.GradeChoices.FAIL
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.exam.exam_name}: {self.marks} ({self.grade})"
