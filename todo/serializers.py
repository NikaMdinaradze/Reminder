from rest_framework import serializers

from todo.validators import ToDoValidator

from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = ToDo
        fields = (
            "id",
            "title",
            "todo",
            "category",
            "created",
            "deadline",
            "owner",
            "active",
        )

    def validate(self, attrs):
        validator = ToDoValidator(**attrs)
        if errors := validator():
            raise serializers.ValidationError(errors)
        return attrs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
