from rest_framework import viewsets, permissions
from rest_framework.pagination import CursorPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from surveys.models import Survey
from surveys.serializer import SurveySerializer


class SurveyPagination(CursorPagination):
    page_size = 20
    ordering = "id"


# Create your views here.
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = SurveyPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
