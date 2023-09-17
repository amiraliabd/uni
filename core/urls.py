from rest_framework.routers import DefaultRouter
from .views import (
    SectionView,
    PendingEvalView,
    StudyingSectionView,
    TeachingSectionView,
    AssistingSectionView,
)


urlpatterns = []

router = DefaultRouter()
# router.register(r'sections', SectionView, basename='sections')
router.register(r'teaching-sections', TeachingSectionView, basename='teaching-sections')
router.register(r'assisting-sections', AssistingSectionView, basename='assisting-sections')
router.register(r'studying-sections', StudyingSectionView, basename='studying-sections')
# router.register(r'pending_eval_sections', PendingEvalView, basename='pending_eval_sections')

urlpatterns += router.urls
