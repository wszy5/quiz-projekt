from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# def home(request):
#     if request.method == 'POST':
#         print(request.POST)
#         questions = QuesModel.objects.all()
#         score = 0
#         wrong = 0
#         correct = 0
#         total = 0
#         for q in questions:
#             total += 1
#             user_answer = request.POST.get(str(q.id)) 
#             print(f"User answer for {q.question}: {user_answer}")
#             print(f"Correct answer: {q.correct_option}")
#             print()
#             if str(q.correct_option) == user_answer: 
#                 score += 10
#                 correct += 1
#             else:
#                 wrong += 1
#         percent = score / (total * 10) * 100
#         context = {
#             'score': score,
#             'time': request.POST.get('timer'),
#             'correct': correct,
#             'wrong': wrong,
#             'percent': percent,
#             'total': total,
#         }
#         return render(request, 'Quiz/result.html', context)
#     else:
#         questions = QuesModel.objects.all()
#         context = {'questions': questions}
#         return render(request, 'Quiz/home.html', context)

def home(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        questions = QuesModel.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            user_answer = request.POST.get(str(q.id)) 
            if str(q.correct_option) == user_answer: 
                score += 1
                correct += 1
            else:
                wrong += 1
        percent = ( score / total ) * 100

        # Zapisujemy wyniki do bazy danych
        quiz_result = QuizResult(
            user=request.user,
            score=score,
            correct=correct,
            wrong=wrong,
            total=total,
            percent=percent,
            time=request.POST.get('timer'),
        )
        quiz_result.save()

        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
        }
        return render(request, 'Quiz/result.html', context)
    else:
        questions = QuesModel.objects.all()
        context = {'questions': questions}
        return render(request, 'Quiz/home.html', context)

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    else: 
        return redirect('home') 


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else: 
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
            else:
                # Możemy dodać feedback w przypadku błędów
                context = {'form': form, 'errors': form.errors}
                return render(request, 'Quiz/register.html', context)
        context = {'form': form}
        return render(request, 'Quiz/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'Quiz/login.html',context)


def login_with_pin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pin = request.POST.get('pin')

        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.pin == pin:
                login(request, user)
                return redirect('home')
            else:
                context = {'error': 'Nieprawidłowy PIN'}
        except User.DoesNotExist:
            context = {'error': 'Użytkownik nie istnieje'}
    else:
        context = {}
    return render(request, 'Quiz/login_with_pin.html', context)

def profile(request):
    # Pobieramy wszystkie wyniki użytkownika
    results = QuizResult.objects.filter(user=request.user).order_by('-created_at')

    # Obliczamy średnią procentową z wyników
    avg_percent = 0
    if results.exists():
        avg_percent = sum([result.percent for result in results]) / len(results)

    context = {
        'results': results,
        'avg_percent': avg_percent,
    }
    return render(request, 'Quiz/profile.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')


