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



User = get_user_model()

class home(View):
    def get(self, request):
        user = request.user
            
        return render(request, "home.html", {'user': user})

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

        user = request.user
        user.xp += score * 100 
        user.level = user.xp // 1000 + 1
        user.save()

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




class profile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        scores = Score.objects.filter(participant=user).order_by('date_participation')
        scores = scores[:5:-1] if len(scores) > 5 else scores[::-1]
        return render(request, 'profile.html', {'user': user,
                                                'scores': scores})
