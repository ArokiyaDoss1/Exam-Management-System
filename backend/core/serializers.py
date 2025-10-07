from rest_framework import serializers
from .models import User, Class, Student, Subject, Exam, Result


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'class_name']


class StudentSerializer(serializers.ModelSerializer):
    class_ref = ClassSerializer(read_only=True)
    class_ref_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), source='class_ref', write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, style={'input_type': 'password'})

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_no', 'class_ref', 'class_ref_id', 'user', 'username', 'password']
        read_only_fields = ['id', 'user', 'class_ref']

    def _generate_unique_username(self, base_username: str) -> str:
        base = base_username.lower().replace(' ', '_') or 'student'
        candidate = base
        suffix = 1
        while User.objects.filter(username=candidate).exists():
            suffix += 1
            candidate = f"{base}{suffix}"
        return candidate

    def create(self, validated_data):
        username = validated_data.pop('username', '').strip() if 'username' in validated_data else ''
        password = validated_data.pop('password', '').strip() if 'password' in validated_data else ''
        name = validated_data.get('name', '').strip()
        roll_no = validated_data.get('roll_no', '').strip()
        if not username:
            base_username = roll_no or name or 'student'
            username = self._generate_unique_username(base_username)
        else:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username': 'Username already exists'})

        user = User(username=username, role=User.Role.STUDENT)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        student = Student.objects.create(user=user, **validated_data)
        return student


class SubjectSerializer(serializers.ModelSerializer):
    class_ref = ClassSerializer(read_only=True)
    class_ref_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), source='class_ref', write_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'class_ref', 'class_ref_id']


class ExamSerializer(serializers.ModelSerializer):
    class_ref = ClassSerializer(read_only=True)
    class_ref_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), source='class_ref', write_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'class_ref', 'class_ref_id', 'exam_date']


class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student', write_only=True)
    exam = ExamSerializer(read_only=True)
    exam_id = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all(), source='exam', write_only=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='subject', write_only=True)

    class Meta:
        model = Result
        fields = ['id', 'student', 'student_id', 'exam', 'exam_id', 'subject', 'subject_id', 'marks', 'grade']
        read_only_fields = ['id', 'grade']

