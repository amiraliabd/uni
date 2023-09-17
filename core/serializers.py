from rest_framework import serializers
from .models import (
    User,
    Section,
    Question,
    Answer,
)
from authentication.serializers import UserSerializer


class SectionSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    assistants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Section
        fields = [
            'id',
            'assistants',
            'teacher',
            'students',
            'class_number',
            'lesson',
            'group',
            'semester',
            'faculty',
        ]

    @staticmethod
    def teaching_sections(user: User):
        return user.teaching_sections.all()

    @staticmethod
    def assistant_sections(user: User):
        return user.assistant_sections.all()

    @staticmethod
    def student_sections(user: User):
        return user.student_sections.filter(is_active=True).all()


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, attrs):
        req_user = self.context.get('request').user
        if req_user.id != attrs.get('student').id:
            raise serializers.ValidationError({'student': 'you cant submit answer for others'})
        return super(AnswerSerializer, self).validate(attrs)


class GiveAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class SectionAnswerSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ['question', 'answer', 'comment']
