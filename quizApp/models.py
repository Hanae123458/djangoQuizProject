from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Participant(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True, 
        default='profile_pictures/default_profile.jpg'
    )
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    bio = models.TextField(max_length=500, blank=True, null=True)
    is_creator = models.BooleanField(blank=False, null=False, default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Categorie(models.Model):
    type_quiz =models.CharField(unique=True,max_length=50)      
    def __str__(self):
        return self.type_quiz

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type_quiz = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    creator = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='quizzes')
    times_played = models.IntegerField(default=0)
    times_visited = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    reponse_1 = models.CharField(max_length=255)
    reponse_2 = models.CharField(max_length=255)
    reponse_3 = models.CharField(max_length=255)
    reponse_4 = models.CharField(max_length=255)
    bonne_reponse = models.IntegerField()

    def __str__(self):
        return self.question_text
    

class Score(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='scores')
    score_final = models.IntegerField()
    date_participation = models.DateField(default=timezone.now)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return f"{self.participant} {self.score_final}/{self.quiz.question_set.count()}"
    
class Question_history(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE, related_name= 'quiz_history')
    user_answer = models.CharField(max_length=255)
    user = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='user_history')
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.question} - {self.user} - {self.time}'