from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from surveys.models import Survey, Question, Choice, Participant, TextResponse, ChoiceUser
from user.models import Person

User = get_user_model()

class SurveyViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass',
            username='testuser'
        )
        self.person = Person.objects.create(
            user=self.user,
            name='Test User',
            sex='M',
            age=30
        )
        self.client.force_authenticate(user=self.user)

        self.survey = Survey.objects.create(
            title='Test Survey',
            small_description='Test Description',
            main_description='Main Description',
            target_number_of_participants=100
        )

    def test_list_surveys(self):
        url = reverse('survey-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_survey(self):
        url = reverse('survey-detail', kwargs={'pk': self.survey.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Survey')

    def test_create_survey(self):
        url = reverse('survey-list')
        data = {
            'title': 'New Survey',
            'small_description': 'New Description',
            'main_description': 'New Main Description',
            'target_number_of_participants': 50,
            'questions': [
                {
                    'text': 'Test Question',
                    'question_type': 'CHOICE',
                    'choices': [
                        {'text': 'Option 1'},
                        {'text': 'Option 2'}
                    ]
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 2)

class SurveyResponseViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass',
            username='testuser'
        )
        self.person = Person.objects.create(
            user=self.user,
            name='Test User',
            sex='M',
            age=30
        )
        self.client.force_authenticate(user=self.user)

        self.survey = Survey.objects.create(
            title='Test Survey',
            small_description='Test Description',
            main_description='Main Description',
            target_number_of_participants=100
        )
        self.question1 = Question.objects.create(
            survey=self.survey,
            text='Multiple Choice Question',
            question_type='CHOICE'
        )
        self.choice1 = Choice.objects.create(question=self.question1, text='Option 1')
        self.choice2 = Choice.objects.create(question=self.question1, text='Option 2')

        self.question2 = Question.objects.create(
            survey=self.survey,
            text='Text Response Question',
            question_type='TEXT_RESPONSE'
        )

    def test_submit_survey_response(self):
        url = reverse('survey-response', kwargs={'survey_id': self.survey.pk})
        data = [
            {'question_id': self.question1.id, 'answer': str(self.choice1.id)},
            {'question_id': self.question2.id, 'answer': 'This is a text response'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(ChoiceUser.objects.count(), 1)
        self.assertEqual(TextResponse.objects.count(), 1)

    def test_submit_survey_response_twice(self):
        url = reverse('survey-response', kwargs={'survey_id': self.survey.pk})
        data = [
            {'question_id': self.question1.id, 'answer': str(self.choice1.id)},
            {'question_id': self.question2.id, 'answer': 'This is a text response'}
        ]
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('이미 참여한 설문조사입니다', str(response.data))

    def test_submit_invalid_survey_response(self):
        url = reverse('survey-response', kwargs={'survey_id': self.survey.pk})
        data = [
            {'question_id': self.question1.id, 'answer': 'invalid_choice_id'},
            {'question_id': self.question2.id, 'answer': 'This is a text response'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid choice for question', str(response.data['error']))

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        url = reverse('survey-response', kwargs={'survey_id': self.survey.pk})
        data = [
            {'question_id': self.question1.id, 'answer': str(self.choice1.id)},
            {'question_id': self.question2.id, 'answer': 'This is a text response'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='newuser@example.com',
            password='newuserpass',
            username='newuser'
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newuserpass'))

    def test_create_user_without_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(password='testpass')

    def test_create_person(self):
        user = User.objects.create_user(
            email='personuser@example.com',
            password='personpass',
            username='personuser'
        )
        person = Person.objects.create(
            user=user,
            name='Person Name',
            sex='F',
            age=25
        )
        self.assertIsNotNone(person)
        self.assertEqual(person.user, user)
        self.assertEqual(person.name, 'Person Name')
        self.assertEqual(person.sex, 'F')
        self.assertEqual(person.age, 25)