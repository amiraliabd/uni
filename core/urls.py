from rest_framework_nested import routers
from .views import (
    SectionView,
    SectionEvalView,
    EvalAnswerView,
)
from django.urls import path, include


router = routers.SimpleRouter()
router.register(r'sections', SectionView, basename='sections')

eval_router = routers.NestedSimpleRouter(router, r'sections', lookup='section')
eval_router.register(r'evaluations', SectionEvalView, basename='section-evaluations')

answer_router = routers.NestedSimpleRouter(eval_router, r'evaluations', lookup='evaluation')
answer_router.register(r'answers', EvalAnswerView, basename='evaluation-answers')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(eval_router.urls)),
    path(r'', include(answer_router.urls)),
]