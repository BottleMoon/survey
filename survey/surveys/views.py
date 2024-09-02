from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from surveys.models import Survey
from surveys.serializer import SurveySerializer, SurveyListSerializer
from surveys.services import SurveyService


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
    # permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return SurveyListSerializer
        else:
            return SurveySerializer


class SurveyResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request, survey_id):
        survey = Survey.objects.get(id=survey_id)
        user = request.user

        return SurveyService.submit_survey_response(user, survey, request)


class SurveyAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, survey_id):
        survey = get_object_or_404(Survey, id=survey_id)
        user = request.user

        return SurveyService.is_survey_available(survey, user)
