from . import views
from django.urls import path
from .views import StatisticsView

urlpatterns=[
                path('', views.quizPage.as_view(), name='quizPageOld'),
                path('start/<int:quiz_id>', views.quizCommence.as_view(), name='quizCommence'),
                path('results/', views.validerReponsesQuiz.as_view() , name='resultatQuiz'),
                path('choice/', views.quizChoice.as_view(), name='quizPage'),
                path('addQuestion/', views.question.as_view(), name="addQuestion"),
                path('create_quiz/', views.CreateQuizView.as_view(), name='create_quiz'),
                path('statistics/', StatisticsView.as_view(), name='statistics'),
                path('question/stats/<int:quizID>', views.question_stats.as_view(), name='quiz_stats'),
                path('question/stats/', views.fetch_quiz_stats.as_view(), name='fetch_quiz'),
            ]
