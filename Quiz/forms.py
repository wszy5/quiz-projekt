from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 

class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"
    
class QuestionCountForm(forms.Form):
    num_questions = forms.IntegerField(
        min_value=1,
        max_value=100,  # Zmienna maksymalna liczba pytań, np. 100
        initial=10,     # Domyślna liczba pytań
        label="Ile pytań chcesz rozwiązać?",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
