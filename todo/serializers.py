from django.utils import timezone
from rest_framework import serializers

from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = ToDo
        fields = ["id", "title", "todo", "created", "deadline", "owner"]

    def validate(self, attrs):
        """
        Check that the creation time is before the deadline.
        """
        if attrs["deadline"] < timezone.now():
            raise serializers.ValidationError("deadline must be after current time")
        return attrs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
