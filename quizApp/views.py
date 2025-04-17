from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .forms import SignUpForm
from .forms import QuizCategoryForm
from .models import Quiz, Categorie
from .models import Score
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

def home(request):
    return render(request, "home.html")

User = get_user_model()

class home(View):
    def get(self, request):
        return render(request, "home.html")

class TraitementFormulaireInscription(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            User = form.save()
            login(request, User)
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

class quizPage(LoginRequiredMixin, View):
    def get(self, request):
        form = QuizCategoryForm()
        return render(request, 'quizPage.html', {'form': form})

class quizChoice(LoginRequiredMixin, View):
    def get(self, request):
        type_quiz = request.GET.get('categorie')
        categories = Categorie.objects.prefetch_related('quiz_set')
        if type_quiz:
            quiz = Quiz.objects.filter(type_quiz__type_quiz=type_quiz)
        else:
            quiz = Quiz.objects.all()
        return render(request, 'quizChoice.html', {'quiz': quiz,
                                                    'categories': categories,
                                                    'type_quiz': type_quiz})

class quizCommence(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.question_set.all()
        return render(request, 'quizCommence.html', {'quiz': quiz, 'questions': questions})

class validerReponsesQuiz(LoginRequiredMixin, View):
    def post(self, request):
        idQuiz = request.POST.get("idQuiz")
        quiz = Quiz.objects.get(id=idQuiz)
        questions = quiz.question_set.all()

        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer and int(user_answer) == question.bonne_reponse:
                score += 1

        scoreObtenu = Score.objects.create(
            participant=request.user,
            score_final=score,
            date_participation=datetime.datetime.now(),
            quiz=quiz
        )
        total = len(questions)
        return render(request, 'resultatQuiz.html', {"user": request.user,
                                                    'quiz': quiz,
                                                    'questions': questions,
                                                    'score': scoreObtenu,
                                                    'total': total
                                                    })





