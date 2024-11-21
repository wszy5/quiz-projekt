# from django.shortcuts import redirect,render
# from django.contrib.auth import login,logout,authenticate
# from .forms import *
# from .models import *
# from django.http import HttpResponse

# # Create your views here.
# def home(request):
#     if request.method == 'POST':
#         print(request.POST)
#         questions=QuesModel.objects.all()
#         score=0
#         wrong=0
#         correct=0
#         total=0
#         for q in questions:
#             total+=1
#             print(request.POST.get(q.question))
#             print(q.ans)
#             print()
#             if q.ans ==  request.POST.get(q.question):
#                 score+=10
#                 correct+=1
#             else:
#                 wrong+=1
#         percent = score/(total*10) *100
#         context = {
#             'score':score,
#             'time': request.POST.get('timer'),
#             'correct':correct,
#             'wrong':wrong,
#             'percent':percent,
#             'total':total
#         }
#         return render(request,'Quiz/result.html',context)
#     else:
#         questions=QuesModel.objects.all()
#         context = {
#             'questions':questions
#         }
#         return render(request,'Quiz/home.html',context)

import random
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        # Pobieranie liczby pytań z formularza
        num_questions = int(request.POST.get('num_questions', 0))
        if num_questions <= 0:
            num_questions = QuesModel.objects.count()  # Domyślnie wszystkie pytania
        
        # Losowanie pytań
        questions = random.sample(list(QuesModel.objects.all()), num_questions)
        
        score = 0
        wrong = 0
        correct = 0
        total = len(questions)
        
        for q in questions:
            answer = request.POST.get(str(q.id))  # Pobieramy odpowiedź na pytanie
            if q.ans == answer:
                score += 10
                correct += 1
            else:
                wrong += 1
        
        percent = (score / (total * 10)) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'Quiz/result.html', context)
    
    else:
        # Dodajemy do kontekstu formularz i pytania
        questions = QuesModel.objects.all()
        form = QuestionCountForm()  # Formularz do wyboru liczby pytań
        context = {
            'questions': questions,
            'form': form
        }
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
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'Quiz/register.html',context)

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

def logoutPage(request):
    logout(request)
    return redirect('/')

