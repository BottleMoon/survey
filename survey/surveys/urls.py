from django.urls import include, path
from rest_framework.routers import SimpleRouter

from surveys.views import SurveyViewSet, SurveyResponseView, SurveyAvailabilityView

router = SimpleRouter()
router.register(r'surveys', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_id>/responses/', SurveyResponseView.as_view(), name='survey-response'),
    path('api/surveys/<int:survey_id>/check-availability/', SurveyAvailabilityView.as_view(), name='survey-availability'),
]