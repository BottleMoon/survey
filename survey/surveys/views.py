from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from surveys.models import Survey
from surveys.serializer import SurveySerializer


# Create your views here.
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
