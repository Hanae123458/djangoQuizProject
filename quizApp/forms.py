from django import forms
from .models import Categorie
from .models import Participant
from .models import Quiz
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','last_name', 'first_name', 'email', 'password1', 'password2']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['last_name', 'first_name', 'email']  

class QuizCategoryForm(forms.Form):
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        empty_label="Sélectionnez une catégorie",
        widget=forms.Select(attrs={'categorie': 'form-control'})
    )

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'type_quiz', 'difficulte']