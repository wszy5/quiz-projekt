from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class createuserform(UserCreationForm):
    pin = forms.CharField(
        max_length=6,
        required=False,  # PIN jest opcjonalny
        widget=forms.PasswordInput(attrs={'placeholder': 'Podaj PIN (opcjonalnie)'}),
        help_text="Opcjonalnie: maksymalnie 6 cyfr"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Tworzymy profil użytkownika i przypisujemy PIN, jeśli podano
            if self.cleaned_data['pin']:
                UserProfile.objects.create(user=user, pin=self.cleaned_data['pin'])
        return user
