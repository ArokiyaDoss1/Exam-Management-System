from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Class, Student, Subject, Exam, Result
from .serializers import (
    UserSerializer,
    ClassSerializer,
    StudentSerializer,
    SubjectSerializer,
    ExamSerializer,
    ResultSerializer,
)
from .permissions import IsAdmin, ReadOnlyOrAdmin


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all().order_by('class_name')
    serializer_class = ClassSerializer
    permission_classes = [ReadOnlyOrAdmin]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('class_ref', 'user').all()
    serializer_class = StudentSerializer
    permission_classes = [ReadOnlyOrAdmin]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('class_ref').all()
    serializer_class = SubjectSerializer
    permission_classes = [ReadOnlyOrAdmin]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('class_ref').all()
    serializer_class = ExamSerializer
    permission_classes = [ReadOnlyOrAdmin]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('student__class_ref', 'exam__class_ref', 'subject__class_ref').all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [ReadOnlyOrAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if getattr(user, 'role', None) == 'STUDENT':
            return qs.filter(student__user_id=user.id)
        return qs
