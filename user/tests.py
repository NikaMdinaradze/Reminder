# your_app/tests/test_serializers.py
from django.contrib.auth.models import User
from django.test import TestCase

from user.serializers import UserCreateSerializer, UserGetSerializer


class UserModelSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "gorgasali",
            "password": "StronkPassword123",
            "email": "vaxtang.gorgasali@yahoo.com",
            "first_name": "vaxtangi",
            "last_name": "farnavaziani",
        }
        self.invalid_datas = [
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
            try:
                self.assertFalse(serializer.is_valid())
            except AssertionError:
                raise AssertionError(
                    f"invalid behaviour for provided data:" f"\n {invalid_data}"
                )

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
