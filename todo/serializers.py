from rest_framework import serializers
from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ToDo
        fields = ['id', 'title', 'todo', 'created', 'deadline','owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
