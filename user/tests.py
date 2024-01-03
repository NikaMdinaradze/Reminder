import copy

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

    valid_data = copy.deepcopy(VALID_DATA)
    invalid_datas = copy.deepcopy(INVALID_DATA)

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
    test class for register endpoint
    """

    url = reverse("user-register")

    def test_register_user(self):
        """
        testing register endpoint with valid data
        """
        data = copy.deepcopy(VALID_DATA)

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_invalid_data(self):
        """
        testing /register/ endpoint with invalid data
        """
        invalid_datas = INVALID_DATA

        for invalid_data in invalid_datas:
            response = self.client.post(self.url, invalid_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserMeTest(APITestCase):
    """
    test class for /user/me endpoint
    """

    def setUp(self):
        self.user = User.objects.create_user(**VALID_DATA)
        self.url = reverse("user-details")

    def test_get_authenticated_user_info(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_update_authenticated_user_info(self):
        self.client.force_authenticate(user=self.user)
        updated_valid_data = VALID_DATA.copy()
        updated_valid_data["username"] = "updated_username"
        data = updated_valid_data

        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_username")

    def test_delete_authenticated_user_info(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_get_unauthenticated_user_info(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_datas = INVALID_DATA

        for invalid_data in invalid_datas:
            response = self.client.put(self.url, invalid_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
