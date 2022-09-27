from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from home.models import *
from .serializers import *
from .permissions import PartecipantGroup


class CustomTokenView(TokenObtainPairView):
    permission_classes = [PartecipantGroup]
    serializer_class = CustomTokenSerializer


class QuizListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the quiz items for the logged user
        '''
        quiz = UserQuiz.objects.filter(
            user=request.user.id, is_complete=False)
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizDetailApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, quiz_id, user_id):
        '''
        Helper method to get the object with given quiz_id, and user_id
        '''
        try:
            return UserQuiz.objects.get(quiz=quiz_id, user=user_id)
        except UserQuiz.DoesNotExist:
            return None

    # Retrieve quiz with specific id
    def get(self, request, quiz_id, *args, **kwargs):
        '''
        Retrieves the Quiz with given quiz_id
        '''
        istance = self.get_object(quiz_id, request.user.id)
        if not istance:
            return Response(
                {"res": "Object with quiz id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = QuizSerializer(istance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizQuestionsListlApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, quiz_id, user_id):
        '''
        Helper method to get the questions with given quiz_id, and user_id
        '''
        try:
            '''
            check if user is allowed to see questions
            '''
            if UserQuiz.objects.filter(quiz=quiz_id, user=user_id).exists():
                return Question.objects.get(quiz=quiz_id)
            return None
        except Question.DoesNotExist:
            return None

    # Retrieve questions with specific quiz id
    def get(self, request, quiz_id, *args, **kwargs):
        '''
        Retrieves the Quiz with given quiz_id
        '''
        istance = self.get_object(quiz_id, request.user.id)
        if not istance:
            return Response(
                {"res": "Object with quiz id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = QuestionsSerializer(istance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizQuestionDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, quiz_id, user_id, question_id):
        '''
        Helper method to get the question with given quiz_id, and user_id
        '''
        try:
            '''
            check if user is allowed to see questions
            '''
            if UserQuiz.objects.filter(quiz=quiz_id, user=user_id).exists():
                return Answer.objects.filter(question=question_id)
            return None
        except Question.DoesNotExist:
            return None

    def get(self, request, quiz_id, question_id, *args, **kwargs):
        '''
        Retrieves the question with given question_id
        '''
        istance = self.get_object(
            quiz_id, request.user.id, question_id)
        if not istance:
            return Response(
                {"res": "Object with quiz id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(istance)
        serializer = AnswerSerializer(istance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create the answer with given data if not present and user is allowed
        '''
        data = {
            'answer': request.data.get('answer_id'),
            'user': request.user.id,

        }
        question_id = Answer.objects.get(
            id=request.data.get('answer_id')).question.id
        quiz_id = Question.objects.get(id=question_id).quiz.id
        serializer = UserAnswerSerializer(data=data)
        if serializer.is_valid():

            if UserQuiz.objects.filter(quiz=quiz_id, user=request.user.id).exists():
                if UserAnswer.objects.filter(answer=request.data.get('answer_id'), user=request.user.id).exists() == False:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
