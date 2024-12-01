"""DjangoQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Quiz.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('addQuestion/', addQuestion,name='addQuestion'),
    path('login/', loginPage,name='login'),
    path('login-pin/', login_with_pin, name='login_with_pin'),
    path('profile/', profile, name='profile'),
    path('logout/', logoutPage,name='logout'),
    path('register/', registerPage,name='register'),
    path('api/questions/', QuesModelAPIView.as_view(), name='api_questions'),
    path('api/questions/<int:pk>/', QuesDetailAPIView.as_view(), name='api_question_detail'),  # Nowa ścieżka
    path('api/users/', UserAPIView.as_view(), name='api_users'),
    path('api/get_csrf_token/', get_csrf_token_view, name='get_csrf_token_view'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
