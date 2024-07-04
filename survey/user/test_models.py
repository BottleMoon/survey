from django.test import TestCase
from .models import User, Person


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123', username='testuser')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.username, 'testuser')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)


class PersonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test2@example.com', password='password123', username='testuser2')
        self.person = Person.objects.create(user=self.user, name='John Doe', sex='M', age=30)

    def test_person_creation(self):
        self.assertEqual(self.person.user, self.user)
        self.assertEqual(self.person.name, 'John Doe')
        self.assertEqual(self.person.sex, 'M')
        self.assertEqual(self.person.age, 30)

    def test_person_string_representation(self):
        self.assertEqual("John Doe", self.person.name)

    def test_person_user_relationship(self):
        self.assertEqual(self.person.user.email, 'test2@example.com')
        self.assertEqual(self.person.user.username, 'testuser2')
