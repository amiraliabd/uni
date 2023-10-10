from datetime import datetime

from django.utils.timezone import make_aware, get_default_timezone

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.serializers import ValidationError
from rest_framework import response, status

from .serializers import (
    SectionSerializer,
    EvaluationListSerializer,
    EvaluationReportSerializer,
    EvaluationDetailSerializer,
    AnswerSerializer,
)
from .models import (
    Evaluation,
)
from .exceptions import HttpNotAllowed


class SectionView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, ]

    def _get_base_query(self):
        user = self.request.user
        if self.action == 'list':
            if qp := self.request.GET.get('role'):
                if qp == 'teacher':
                    return user.teaching_sections
                elif qp == 'assistant':
                    return user.assistant_sections
                elif qp == 'student':
                    return user.student_sections
                else:
                    raise ValidationError({"role": "only teacher or assistant or student"})

        return user.student_sections.union(user.teaching_sections.all()).union(user.assistant_sections.all())

    def get_queryset(self):
        if qp := self.request.GET.get('is_active', None):
            if qp == 'true':
                is_active = True
            elif qp == 'false':
                is_active = False
            else:
                raise ValidationError({"is_active": "only true or false"})
            return self._get_base_query.filter(is_active=is_active).all()

        return self._get_base_query().all()


class SectionEvalView(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Evaluation.objects.filter(section__id=self.kwargs['section_pk']).all()

    def get_object(self):
        obj = super(SectionEvalView, self).get_object()

        answered_questions = self.request.user.answers.filter(evaluation__id=obj.id).all()

        # if all questions are not answered let user answer again
        if len(answered_questions) < len(obj.questions.all()):
            return obj
        else:
            # user must wait till evaluation report is ready
            raise HttpNotAllowed('you should waite till deadline to get evaluation report')

    def get_serializer_class(self):
        if self.action == 'list':
            return EvaluationListSerializer
        else:
            evaluation = self.get_object()
            if evaluation.deadline < make_aware(datetime.now(), get_default_timezone()):
                return EvaluationReportSerializer
            else:
                if evaluation.section.id in [s.id for s in self.request.user.student_sections.all()]:
                    return EvaluationDetailSerializer
                else:
                    # user is teacher or assistant so must wait till evaluation report is ready
                    raise HttpNotAllowed('you should waite till deadline to get evaluation report')

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super(SectionEvalView, self).retrieve(request, *args, **kwargs)
        except HttpNotAllowed as err:
            return err.http_response
        return response


class EvalAnswerView(GenericViewSet):

    permission_classes = [IsAuthenticated, ]
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return response.Response(status=status.HTTP_201_CREATED)
