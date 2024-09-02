from django.db import transaction
from rest_framework import serializers

from surveys.models import Survey, Question, Choice, ChoiceUser, Participant


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'choices']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Survey
        fields = ['id', 'title', 'created_at', 'small_description', 'main_description', 'target_number_of_participants', 'classification', 'questions']

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('question_set')
        survey = Survey.objects.create(**validated_data)
        for question_data in questions_data:
            choices_data = question_data.pop('choice_set')
            question = Question.objects.create(survey=survey, **question_data)
            if question_data.get('question_type') == 'CHOICE':
                for choice_data in choices_data:
                    Choice.objects.create(question=question, **choice_data)
        return survey


class SurveyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ['id', 'title', 'small_description', 'target_number_of_participants', 'participants_count', 'classification']


class SurveyResponseSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()