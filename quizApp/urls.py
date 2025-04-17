from . import views
from django.urls import path

urlpatterns=[
                path('', views.quizPage.as_view(), name='quizPage'),
                path('start/', views.quizCommence.as_view(), name='quizCommence'),
                path('results/', views.validerReponsesQuiz.as_view() , name='resultatQuiz'),
            ]
