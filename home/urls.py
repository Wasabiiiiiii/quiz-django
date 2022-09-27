from django.urls import path
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    path("", indexView.as_view(), name="index"),
    path("<int:myid>/", quizView.as_view(), name="quiz"),
    path('<int:myid>/data/', quizdataView.as_view(), name='quiz-data'),
    path('<int:myid>/save/', quizsaveView.as_view(), name='quiz-save'),
    url(r'^accounts/', include('allauth.urls')),
    path('invitation/', invitationView.as_view(), name='invitation'),
    path('add_quiz/', addquizView.as_view(), name='add_quiz'),
    path('add_user_quiz/', adduserquizView.as_view(), name='add_quiz'),
    path('add_question/', addquestionView.as_view(), name='add_question'),
    path('add_options/<int:myid>/', addoptionView.as_view(), name='add_options'),
    path('results/', resultsView.as_view(), name='results'),
    path('delete_question/<int:myid>/',
         deletequestionView.as_view(), name='delete_question'),
    path('delete_result/<int:myid>/', indexView.as_view, name='delete_result'),
    path('send_results/<int:my_id>/<int:user_id>/',
         sendResultsView.as_view(), name='send_results'),
]
