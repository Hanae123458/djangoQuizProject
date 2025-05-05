from django.contrib import admin
from .models import Participant,Categorie,Quiz,Question,Score, Question_history

admin.site.register(Participant)
admin.site.register(Categorie)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(Question_history)
