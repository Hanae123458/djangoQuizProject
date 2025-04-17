from . import views
from django.urls import path

urlpatterns=[
                path('', views.quizPage, name='quizPage'),
                path('start/', views.quizCommence, name='quizCommence'),
                path('results/', views.validerReponsesQuiz , name='resultatQuiz'),
            ]
