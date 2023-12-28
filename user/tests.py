from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.serializers import UserCreateSerializer, UserGetSerializer

VALID_DATA = {
    "username": "gorgasali",
    "password": "StronkPassword123",
    "email": "vaxtang.gorgasali@yahoo.com",
    "first_name": "vaxtangi",
    "last_name": "farnavaziani",
}

INVALID_DATA = [
    {
        "username": "",
        "password": "StronkPassword123",
        "email": "vaxtang.gorgasali@yahoo.com",
        "first_name": "vaxtangi",
        "last_name": "farnavaziani",
    },
    {
        "username": "gorgasali",
        "password": "",
        "email": "vaxtang.gorgasali@yahoo.com",
        "first_name": "vaxtangi",
        "last_name": "farnavaziani",
    },
]


class UserModelSerializerTest(TestCase):
    """
    test class for user's serializers
    """

    def setUp(self):
        self.valid_data = VALID_DATA
        self.invalid_datas = INVALID_DATA

    def test_valid_serializer_data(self):
        """
        testing UserCreate serializer with valid data
        """

        serializer = UserCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        """
        testing UserCreate serializer with invalid datas
        """

        for invalid_data in self.invalid_datas:
            serializer = UserCreateSerializer(data=invalid_data)
            self.assertFalse(serializer.is_valid())

    def test_serialization(self):
        """
        testing UserGetSerializer
        """
        instance = User.objects.create(**self.valid_data)
        serializer = UserGetSerializer(instance)
        expected_data = {
            "username": "gorgasali",
            "first_name": "vaxtangi",
            "last_name": "farnavaziani",
            "email": "vaxtang.gorgasali@yahoo.com",
        }

        self.assertEqual(serializer.data, expected_data)


class RegisterTest(APITestCase):
    """
    test class for user's view
    """

    url = reverse("user-register")

    def test_register_user(self):
        """
        testing register endpoint with valid data
        """
        data = VALID_DATA

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_invalid_data(self):
        """
        testing register endpoint with invalid data
        """
        invalid_datas = INVALID_DATA

        for invalid_data in invalid_datas:
            response = self.client.post(self.url, invalid_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
