from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.decorators import action
from .serializers import (
    SectionSerializer,
    QuestionSerializer,
    SectionAnswerSerializer,
    GiveAnswerSerializer
)
from .models import (
    Section,
    PendingEvaluation,
    Answer,
)


class BaseSectionView(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, ]

    def _get_base_query(self):
        raise NotImplementedError

    def get_queryset(self):
        if qp := self.request.GET.get('is_active', None):
            if qp == 'true':
                is_active = True
            else:
                is_active = False
            return self._get_base_query.filter(is_active=is_active).all()

        return self._get_base_query.all()

    def list(self, request, *args, **kwargs):
        if qp := self.request.GET.get('is_active', None):
            if qp not in ['true', 'false']:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data='is_active query param must be true or false'
                )
        return super().list(request, *args, **kwargs)


class StudyingSectionView(BaseSectionView):
    def _get_base_query(self):
        return self.request.user.student_sections


class AssistingSectionView(BaseSectionView):
    def _get_base_query(self):
        return self.request.user.assistant_sections


class TeachingSectionView(BaseSectionView):
    def _get_base_query(self):
        return self.request.user.teaching_sections


class SectionView(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return user.student_sections

    @action(detail=True,
            methods=['get', ],
            serializer_class=QuestionSerializer,
            )
    def evaluate(self, request, pk=None):
        user_section = Section.objects.filter(
            students__id=self.request.user.id,
            id=pk
        ).first()
        if not user_section:
            return Response('you are not registered in this section',
                            status=status.HTTP_400_BAD_REQUEST)
        answered_eval = Answer.objects.filter(
            student__id=self.request.user.id,
            section__id=user_section.id
        ).all()
        user_pending_eval = PendingEvaluation.objects.filter(
            section__id=user_section.id
        ).exclude(
            question__id__in=[i.question.id for i in answered_eval]
        )
        serializer = self.serializer_class([i.question for i in user_pending_eval],
                                           many=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post', ],
            serializer_class=GiveAnswerSerializer,
            )
    def answer(self, request, pk=None):
        request.data['student'] = request.user.id
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response('answer submitted')
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['get', ],
            )
    def evaluation_responses(self, request, pk=None):
        section = self.get_object()
        section_eval = section.evals.all().order_by('question')
        serializer = SectionAnswerSerializer(section_eval, many=True)
        return Response(serializer.data)


class PendingEvalView(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user_sections = Section.objects.filter(students__id=self.request.user).all()
        pending_eval = PendingEvaluation.objects.filter(
            section__in=[i.id for i in user_sections]
        ).all()
        answered_eval = Answer.objects.filter(
            student__id=2,
            section__id__in=[i.id for i in pending_eval]
        ).all()
        user_pending_eval = PendingEvaluation.objects.filter(
            section__in=[i.id for i in user_sections]
        ).exclude(
            id__in=[i.id for i in answered_eval]
        ).all()
        user_section_pending_eval = Section.objects.filter(
            id__in=[i.section.id for i in user_pending_eval]
        )

        return user_section_pending_eval
