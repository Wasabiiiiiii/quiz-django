from rest_framework import serializers
from home.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenSerializer, cls).get_token(user)

        # Add username claims
        token['username'] = user.username
        return token


class QuizSerializer(serializers.ModelSerializer):
    quiz_name = serializers.CharField(source='quiz.name',)

    class Meta:
        model = UserQuiz()
        fields = ['quiz', 'is_complete', 'quiz_name']


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question()
        fields = ['id', 'content', ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer()
        fields = ['id', 'content']


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = "__all__"
