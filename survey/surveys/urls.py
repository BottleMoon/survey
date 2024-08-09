from django.urls import include, path
from rest_framework.routers import SimpleRouter

from surveys.views import SurveyViewSet

router = SimpleRouter()
router.register(r'surveys', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]