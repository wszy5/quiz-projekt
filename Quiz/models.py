from django.db import models
from django.contrib.auth.models import User


class QuesModel(models.Model):
    question = models.CharField(max_length=200, null=True, verbose_name="Pytanie")
    op1 = models.CharField(max_length=200, null=True, verbose_name="Opcja 1")
    op2 = models.CharField(max_length=200, null=True, verbose_name="Opcja 2")
    op3 = models.CharField(max_length=200, null=True, verbose_name="Opcja 3")
    correct_option = models.PositiveSmallIntegerField(
        choices=[
            (1, "Opcja 1"),
            (2, "Opcja 2"),
            (3, "Opcja 3"),
            (4, "Opcja 4"),
        ],
        verbose_name="Poprawna opcja",
        default=1
    )

    def __str__(self):
        return self.question

    def get_correct_answer(self):
        """Zwraca tekst poprawnej odpowiedzi."""
        return getattr(self, f'op{self.correct_option}')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6, null=True, blank=True) 

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Powiązanie z użytkownikiem
    score = models.IntegerField()  # Wynik
    correct = models.IntegerField()  # Liczba poprawnych odpowiedzi
    wrong = models.IntegerField()  # Liczba błędnych odpowiedzi
    total = models.IntegerField()  # Całkowita liczba pytań
    percent = models.FloatField()  # Procent poprawnych odpowiedzi
    time = models.IntegerField()  # Czas rozwiązania quizu (w sekundach)
    created_at = models.DateTimeField(auto_now_add=True)  # Data wykonania quizu

    def __str__(self):
        return f'Wyniki dla {self.user.username} z dnia {self.created_at}'