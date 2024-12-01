from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import QuesModel
from .serializers import QuesModelSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Quiz.models import QuesModel

def get_csrf_token_view(request):
    return JsonResponse({'csrftoken': get_token(request)})

# Widok dla pytań
class QuesModelAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        questions = QuesModel.objects.all()
        serializer = QuesModelSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuesDetailAPIView(APIView):
   
    def get_object(self, pk):
        try:
            return QuesModel.objects.get(pk=pk)
        except QuesModel.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuesModelSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuesModelSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_object(pk)
        if not question:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionDetail(APIView):
    def delete(self, request, id, format=None):
        try:
            question = QuesModel.objects.get(pk=id)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QuesModel.DoesNotExist:
            return Response({'error': 'Pytanie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
        
# Widok dla użytkowników
class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

#------------------------------------------------------------------------------------------------------
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


