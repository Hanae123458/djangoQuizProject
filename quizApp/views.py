from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,get_user_model
from django.contrib import messages
from .forms import SignUpForm
from .forms import QuizCategoryForm
from .models import Quiz
from .models import Score
import datetime

def home(request):
    return render(request,"home.html")

User = get_user_model()

def TraitementFormulaireInscription(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            User = form.save()
            login(request, User)  
            return redirect('login') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def quizPage(request):
    form = QuizCategoryForm()
    return render(request, 'quizPage.html', {'form': form})


def quizCommence(request):
    quiz = get_object_or_404(Quiz, type_quiz=request.GET.get('categorie'))
    questions = quiz.question_set.all()
    return render(request, 'quizCommence.html', {'quiz': quiz, 'questions': questions})


def validerReponsesQuiz(request):
    if request.method == "POST":
        idQuiz = request.POST.get("idQuiz")
        quiz = Quiz.objects.get(id=idQuiz)
        questions = quiz.question_set.all()
        
        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer and int(user_answer) == question.bonne_reponse:
                score += 1


        scoreObtenu=Score.objects.create(
            participant=request.user,
            score_final=score,
            date_participation=datetime.datetime.now(),
            quiz=quiz
        )
        total=len(questions)
        
        
    return render(request, 'resultatQuiz.html', {"user":request.user,'quiz': quiz, 'questions': questions,'score':scoreObtenu,'total':total})
    
    
        


