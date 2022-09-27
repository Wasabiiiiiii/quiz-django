from django.urls import reverse, resolve
from django.test import SimpleTestCase
from quiz_api.views import QuizListApiView
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from home.models import UserQuiz, Quiz, Answer, Question
from rest_framework import status
from quiz_api.permissions import PartecipantGroup


class ApiUrlsTests(SimpleTestCase):

    def test_quiz_is_resolved(self):
        url = reverse('partecipant-quizzes')
        self.assertEquals(resolve(url).func.view_class, QuizListApiView)


class QuizListApiViewTests(APITestCase):
    quiz_url = reverse('partecipant-quizzes')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apitest', password='hashpw13456')
        partecipant = Group.objects.get_or_create(name="partecipant")
        partecipant_group = Group.objects.get(name='partecipant')
        partecipant_group.user_set.add(self.user)
        self.quiz = Quiz.objects.create(name='quizapi', desc='testdesc')
        self.user_quiz = UserQuiz.objects.create(
            quiz=self.quiz, user=self.user, )

    def tearDown(self):
        pass

    def test_get_quizzes_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quizzes_not_auth(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 401)


class QuizDetailApiViewTests(APITestCase):
    quiz_url = reverse('partecipant-quiz', kwargs={'quiz_id': 1})

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apitest', password='hashpw13456')
        partecipant = Group.objects.get_or_create(name="partecipant")
        partecipant_group = Group.objects.get(name='partecipant')
        partecipant_group.user_set.add(self.user)
        self.quiz = Quiz.objects.create(name='quizapi', desc='testdesc')
        self.user_quiz = UserQuiz.objects.create(
            quiz=self.quiz, user=self.user, )

    def tearDown(self):
        pass

    def test_get_quiz_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quiz_not_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 401)


class QuizQuestionDetailApiView(APITestCase):
    quiz_url = reverse('partecipant-quiz-question-answer',
                       kwargs={'quiz_id': 1, 'question_id': 1})

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apitest', password='hashpw13456')
        partecipant = Group.objects.get_or_create(name="partecipant")
        partecipant_group = Group.objects.get(name='partecipant')
        partecipant_group.user_set.add(self.user)
        self.quiz = Quiz.objects.create(name='quizapi', desc='testdesc')
        self.question = Question.objects.create(content='1+1?', quiz=self.quiz)
        self.answer = Answer.objects.create(
            content='2', correct=True, question=self.question)
        self.user_quiz = UserQuiz.objects.create(
            quiz=self.quiz, user=self.user, )

    def tearDown(self):
        pass

    def test_get_quiz_answers_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quiz_answers_not_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 401)

    def test_post_quiz_answer_auth(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "answer_id": 1,
            'user': 1
        }
        response = self.client.post(self.quiz_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 1)

    def test_post_quiz_answer_not_auth(self):
        self.client.force_authenticate(user=None)
        data = {
            "answer_id": 1,
            'user': 1
        }
        response = self.client.post(self.quiz_url, data, format='json')
        self.assertEqual(response.status_code, 401)
