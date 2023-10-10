from rest_framework import serializers
from .models import (
    User,
    Section,
    Question,
    Answer,
    Evaluation,
)
from django.db import IntegrityError


class SectionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'description',
                  'father_name',
                  'biography',
                  'website',
                  'linkedin',
                  'telegram',
                  'has_safe_pass',
                  'entering_year',
                  'field',
                  ]


class SectionSerializer(serializers.ModelSerializer):
    teacher = SectionUserSerializer(read_only=True)
    assistants = SectionUserSerializer(read_only=True, many=True)

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


class AnswerQuestionSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.IntegerField()


class AnswerSerializer(serializers.Serializer):
    answers = AnswerQuestionSerializer(many=True)

    def create(self, validated_data):
        student = self.context["request"].user

        evaluation_id = self.context["view"].kwargs['evaluation_pk']
        evaluation = Evaluation.objects.get(id=evaluation_id)

        for answer in validated_data['answers']:
            try:
                obj, created = Answer.objects.update_or_create(
                    question=Question.objects.get(id=answer['question']),
                    defaults={'answer': answer['answer'],
                              'student': student,
                              'evaluation': evaluation})
            except IntegrityError:
                raise serializers.ValidationError(
                    {"question": "you have already answered to this question"})


class EvaluationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['title', 'deadline', 'id']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question', 'id']


class EvaluationDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Evaluation
        fields = ['title', 'deadline', 'questions']


class EvaluationReportSerializer:
    # Todo: How to handle evaluation report?
    pass

