from . import views
from django.urls import path

urlpatterns=[
                path("", views.home, name="quizApp_home"),
                path("quizPage/", views.quizPage, name="quizApp_quizPage"),
                path("quizCommence/", views.quizCommence, name="quizApp_quizCommence"),
                path("resultatQuiz/", views.validerReponsesQuiz, name="quizApp_validerReponsesQuiz"),
                path("", views.TraitementFormulaireInscription, name="quizApp_TraitementFormulaireInscription"),
                path("", views.login, name="quizApp_login"),
            ]
