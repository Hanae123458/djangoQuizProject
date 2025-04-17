from . import views
from django.urls import path

urlpatterns=[
                path('', views.quizPage.as_view(), name='quizPageOld'),
                path('start/<int:quiz_id>', views.quizCommence.as_view(), name='quizCommence'),
                path('results/', views.validerReponsesQuiz.as_view() , name='resultatQuiz'),
                path('choice/', views.quizChoice.as_view(), name='quizPage'),
                
            ]
