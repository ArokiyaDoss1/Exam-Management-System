from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Class, Student, Subject, Exam, Result


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Show role in list
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    # Add role to the existing fieldsets
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    # Add role to the add form as well (optional; role will default to STUDENT if omitted)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Role', {'classes': ('wide',), 'fields': ('role',)}),
    )

    # Inline Student profile on User
    class StudentInline(admin.StackedInline):
        model = Student
        can_delete = False
        extra = 0

    inlines = [StudentInline]


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name')
    search_fields = ('class_name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll_no', 'class_ref', 'user')
    list_filter = ('class_ref',)
    search_fields = ('name', 'roll_no', 'user__username', 'user__email')
    autocomplete_fields = ('user', 'class_ref')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'class_ref')
    list_filter = ('class_ref',)
    search_fields = ('subject_name',)
    autocomplete_fields = ('class_ref',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_name', 'class_ref', 'exam_date')
    list_filter = ('class_ref', 'exam_date')
    search_fields = ('exam_name',)
    autocomplete_fields = ('class_ref',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'exam', 'subject', 'marks', 'grade')
    list_filter = ('exam', 'subject', 'grade')
    search_fields = ('student__name', 'exam__exam_name', 'subject__subject_name')
