from rest_framework.routers import DefaultRouter
from .views import SectionView, PendingEvalView


urlpatterns = []

router = DefaultRouter()
router.register(r'sections', SectionView, basename='sections')
router.register(r'pending_eval_sections', PendingEvalView, basename='pending_eval_sections')

urlpatterns += router.urls
