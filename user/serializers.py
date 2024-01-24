import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def save_cached(self):
        """Saves User Information in Cache and Returns Redis Key"""
        data = self.validated_data
        key = uuid.uuid4()
        cache.set(key, data)
        return key
