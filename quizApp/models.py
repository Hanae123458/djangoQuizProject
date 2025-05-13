from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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
    DIFFICULTE_CHOICES = [
        ('Facile', 'Facile'),
        ('Moyen', 'Moyen'),
        ('Difficile', 'Difficile'),
    ]
    difficulte = models.CharField(max_length=10, choices=DIFFICULTE_CHOICES, default='Facile')
    title = models.CharField(max_length=255)
    description = models.TextField()
    type_quiz = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    creator = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='quizzes')
    times_played = models.IntegerField(default=0)
    times_visited = models.IntegerField(default=0)
    def __str__(self):
        return self.title

# Résolution du conflit Git dans le modèle Question
class Question(models.Model):
    TYPE_CHOICES = [
        ('QCM', 'QCM'),
        ('VF', 'Vrai/Faux'),
        ('RC', 'Réponse courte'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    type_question = models.CharField(max_length=3, choices=TYPE_CHOICES, default='QCM')
    reponse_1 = models.CharField(max_length=255)
    reponse_2 = models.CharField(max_length=255, blank=True)
    reponse_3 = models.CharField(max_length=255, blank=True)
    reponse_4 = models.CharField(max_length=255, blank=True)
    bonne_reponse = models.IntegerField()

    def __str__(self):
        return self.question_text

    def clean(self):
        super().clean()
        if self.type_question == "VF":
            if self.reponse_3 or self.reponse_4:
                raise ValidationError("Type Vrai/Faux : Réponse 3 et 4 doivent être vides.")
        elif self.type_question == "QCM":
            if not self.reponse_3 or not self.reponse_4:
                raise ValidationError("Type QCM : les quatre réponses sont requises.")
        elif self.type_question == "RC":
            if self.reponse_2 or self.reponse_3 or self.reponse_4:
                raise ValidationError("Type Réponse courte : seule Réponse 1 doit être utilisée.")

    

class Score(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='scores')
    score_final = models.IntegerField()
    date_participation = models.DateField(default=timezone.now)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return f"{self.participant} {self.score_final}/{self.quiz.question_set.count()}"
    
class Question_history(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE, related_name= 'history')
    user_answer = models.CharField(max_length=255)
    user = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='history')
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.question} - {self.user} - {self.time}'