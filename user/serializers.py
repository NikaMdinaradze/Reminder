from django.contrib.auth.models import User
from rest_framework import serializers
from todo.models import ToDo
class UserGetSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(many=True, queryset=ToDo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'todos']

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password','email', 'first_name', 'last_name']