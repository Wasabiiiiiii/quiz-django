from django.conf.urls import url
from django.urls import path, include
from .views import (
    QuizListApiView,
    QuizDetailApiView,
    QuizQuestionsListlApiView,
    QuizQuestionDetailApiView,

)

urlpatterns = [
    path('quiz/', QuizListApiView.as_view(), name='partecipant-quizzes'),
    path('quiz/<int:quiz_id>/', QuizDetailApiView.as_view(),
         name='partecipant-quiz'),
    path('quiz/<int:quiz_id>/questions/',
         QuizQuestionsListlApiView.as_view(), name='partecipant-quiz-questions'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/',
         QuizQuestionDetailApiView.as_view(), name='partecipant-quiz-question-answer'),

]
