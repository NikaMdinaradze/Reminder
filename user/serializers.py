import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import serializers

from user.validators import UserValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def validate(self, attrs):
        validator = UserValidator(**attrs)
        if errors := validator.perform_check():
            raise serializers.ValidationError(errors)
        return attrs

    def save_cached(self):
        """Saves User Information in Cache and Returns Redis Key"""
        data = self.validated_data
        key = uuid.uuid4()
        cache.set(key, data, timeout=24 * 60 * 60)  # 24 hours
        return key
