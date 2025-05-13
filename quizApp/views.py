from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .forms import SignUpForm
from .forms import QuizCategoryForm
from .models import Quiz, Categorie, Question, Question_history
from .models import Score
import datetime
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import QuizForm
from django.db.models import Avg, Max, Min
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class LoginViewCustom(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get('role')  # Récupère le rôle coché

        if form.is_valid():
            user = form.get_user()

            # Met à jour le champ is_creator en fonction du rôle
            if role == 'createur':
                user.is_creator = True
            else:
                user.is_creator = False

            user.save()

            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'form': form})

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
        difficulte = request.GET.get('difficulte')

        categories = Categorie.objects.all()
        quiz = Quiz.objects.all()

        if type_quiz:
            quiz = quiz.filter(type_quiz__type_quiz=type_quiz)
        if difficulte:
            quiz = quiz.filter(difficulte__iexact=difficulte)

        return render(request, 'quizChoice.html', {
            'quiz': quiz,
            'categories': categories,
            'type_quiz': type_quiz,
            'difficulte': difficulte,
        })


class quizCommence(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.times_visited+=1
        quiz.save()
        questions =quiz.questions.all()
        return render(request, 'quizCommence.html', {'quiz': quiz, 'questions': questions})

class validerReponsesQuiz(LoginRequiredMixin, View):
    def post(self, request):
        idQuiz = request.POST.get("idQuiz")
        quiz = Quiz.objects.get(id=idQuiz)
        quiz.times_played+=1
        quiz.save()
        questions = quiz.questions.all()

        score = 0
        user_answers = []
        for question in questions:
            if question.type_question == 'QCM':
                user_answer = request.POST.get(str(question.id))
                history = Question_history.objects.create(
                    question = question,
                    user_answer = user_answer,
                    user = request.user
                )
                history.save()
                print(str(question.id))
                user_answers.append({"question" : question,
                                    "user_answer" : int(user_answer)})
                if user_answer and int(user_answer) == question.bonne_reponse:
                    score += 1
            else :
                user_answer = request.POST.get(str(question.id))
                history = Question_history.objects.create(
                    question = question,
                    user_answer = user_answer,
                    user = request.user
                )
                history.save()
                user_answers.append({"question" : question,
                                    "user_answer" : (user_answer)
                            
                                    })
                
                if user_answer and user_answer == question.reponse_1:
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
                                                    'total': total,
                                                    "user_answers":user_answers
                                                    })

class CreateQuizView(LoginRequiredMixin, FormView):
    template_name = 'create_quiz.html'
    form_class = QuizForm

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'is_creator', False):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.creator = self.request.user
        quiz.save()
        return render(self.request, 'add_questions.html', {
            "user": self.request.user,
            "quiz": quiz
        })

class profile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        scores = Score.objects.filter(participant=user).order_by('date_participation')
        scores = scores[:5:-1] if len(scores) > 5 else scores[::-1]
        return render(request, 'profile.html', {'user': user,
                                                'scores': scores})


class StatisticsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        scores = Score.objects.filter(participant=user).order_by('date_participation')
        average_score = scores.aggregate(Avg('score_final'))['score_final__avg'] or 0
        max_score = scores.aggregate(Max('score_final'))['score_final__max'] or 0
        min_score = scores.aggregate(Min('score_final'))['score_final__min'] or 0

        return render(request, 'statistics.html', {
            'scores': scores,
            'average_score': average_score,
            'max_score': max_score,
            'min_score': min_score
        })

class question(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 
            qID = int(data.get('quizID'))

            quiz = Quiz.objects.get(id=qID)

            Question.objects.create(
                quiz=quiz,
                question_text=data.get('question_text'),
                type_question = data.get('type_question'),
                reponse_1=data.get('reponse_1'),
                reponse_2=data.get('reponse_2'),
                reponse_3=data.get('reponse_3'),
                reponse_4=data.get('reponse_4'),
                bonne_reponse=data.get('bonne_reponse'),
            )

            return JsonResponse({'status': 'success'})

        except Quiz.DoesNotExist:
            return JsonResponse({'error': 'Quiz not found'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)


class question_stats(View):
    def get(self, request, quizID):
        quiz = Quiz.objects.get(id = quizID)
        data = []
        questions = quiz.questions.all()
        for question in questions : 
            answers = question.history.all()
            right_answers = 0
            answer_counter = {}
            for answer in answers : 
                # Count frequency for most_frequent_answer
                ans_val = (answer.user_answer or '').strip().lower()
                if ans_val:
                    answer_counter[ans_val] = answer_counter.get(ans_val, 0) + 1
                # Handle different types of questions (QCM, VF, RC)
                if question.type_question == 'QCM':
                    if answer.user_answer and str(answer.user_answer) == str(question.bonne_reponse):
                        right_answers += 1
                elif question.type_question == 'VF':
                    bonne = str(question.reponse_1).strip().lower()
                    user_val = str(answer.user_answer).strip().lower()
                    if user_val == bonne:
                        right_answers += 1
                elif question.type_question == 'RC':
                    if answer.user_answer and answer.user_answer.strip().lower() == (question.reponse_1 or '').strip().lower():
                        right_answers += 1
            # Find most frequent answer
            if answer_counter:
                most_frequent_answer = max(answer_counter.items(), key=lambda x: x[1])[0]
            else:
                most_frequent_answer = None
            proportion = round((right_answers / len(answers)) * 100, 0) if len(answers) > 0 else '_'
            data.append({
                'text' : question.question_text,
                'right_answers': right_answers,
                'bad_answers' : len(answers)-right_answers,
                'proportion': proportion,
                'most_frequent_answer': most_frequent_answer
            })
        return render(request, 'question_stats.html', {
            'questions':data,
            "quizzes" :  Quiz.objects.all()
        })
    def post(self, request):
        self.get(self, request, request.POST.get(id))

class fetch_quiz_stats(View):
    def get(self, request) :
        quizzes = Quiz.objects.all()
        return render(request, "select_quiz_stats.html", {
            "quizzes" : quizzes
        })