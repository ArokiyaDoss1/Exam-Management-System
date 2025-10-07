from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN')


class IsStudentSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Students can access only their own data
        if getattr(request.user, 'role', None) == 'STUDENT':
            # obj could be Student or Result
            if hasattr(obj, 'user_id'):
                return obj.user_id == request.user.id
            if hasattr(obj, 'student_id') and hasattr(obj.student, 'user_id'):
                return obj.student.user_id == request.user.id
        return False


class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN')

