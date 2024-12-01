from rest_framework import serializers
from .models import QuesModel
from django.contrib.auth.models import User

class QuesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuesModel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']