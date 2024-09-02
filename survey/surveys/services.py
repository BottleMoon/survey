from rest_framework import status
from rest_framework.response import Response

from surveys.models import Participant, Question, TextResponse, Choice, ChoiceUser, Survey
from surveys.serializer import SurveyResponseSerializer


class SurveyService:
    @staticmethod
    def submit_survey_response(user, survey, request):

        if Participant.objects.filter(survey=survey, user=user).exists():
            return Response({"message": "이미 참여한 설문조사입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if survey.is_complete:
            return Response({"message": "완료된 설문조사입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SurveyResponseSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        Participant.objects.create(survey=survey, user=user)

        text_responses = []
        choice_responses = []

        for item in serializer.validated_data:
            question = Question.objects.get(id=item['question_id'])
            if question.survey != survey:
                return Response({"error": "잘못된 요청입니다. (survey and question not matched)"}, status=status.HTTP_400_BAD_REQUEST)

            if question.question_type == 'TEXT_RESPONSE':
                # TextResponse.objects.create(
                #     question=question,
                #     user=user,
                #     text=item['answer']
                # )
                text_responses.append(TextResponse(question=question, user=user,text=item['text']))

            elif question.question_type == 'CHOICE':
                try:
                    choice_id = int(item['answer'])
                    choice = Choice.objects.get(id=choice_id, question=question)
                    # ChoiceUser.objects.create(
                    #     question=question,
                    #     choice=choice,
                    #     user=user
                    # )
                    choice_responses.append(ChoiceUser(question=question, choice=choice, user=user))
                except (ValueError, Choice.DoesNotExist):
                    return Response({"error": f"Invalid choice for question {question.id}"}, status=status.HTTP_400_BAD_REQUEST)
        TextResponse.objects.bulk_create(text_responses)
        ChoiceUser.objects.bulk_create(choice_responses)

        survey.participants_count += 1
        survey.save()

        return Response({"message": "설문 응답이 성공적으로 제출되었습니다."}, status=status.HTTP_201_CREATED)

    @staticmethod
    def is_survey_available(self, survey, user):
        if Participant.objects.filter(user=user, survey=survey).exists():
            return Response({"message": "Survey is already participating"}, status=status.HTTP_400_BAD_REQUEST)
        if survey.is_complete:
            return Response({"message": "Survey is already complete"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Survey is available"}, status=status.HTTP_200_OK)