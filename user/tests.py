import uuid
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.factories import UserPayloadFactory


class RegisterViewTests(TestCase):
    url = reverse("user-register")

    def setUp(self):
        self.client = APIClient()

    @patch("user.views.send_verification_email.delay")
    @patch("user.views.UserSerializer.save_cached")
    def test_registration_with_valid_data(self, mocked_cache, mocked_mail):
        mocked_cache.return_value = uuid.uuid4()
        mocked_mail.return_value = None
        data = UserPayloadFactory().write_only_payload()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("user.views.send_verification_email.delay")
    @patch("user.views.UserSerializer.save_cached")
    def test_registration_with_invalid_data(self, mocked_cache, mocked_mail):
        mocked_cache.return_value = uuid.uuid4()
        mocked_mail.return_value = None
        invalid_data = [
            UserPayloadFactory(username=""),
            UserPayloadFactory(password=""),
            UserPayloadFactory(email=""),
            UserPayloadFactory(first_name=""),
            UserPayloadFactory(last_name=""),
            UserPayloadFactory(email="invalidemail"),
        ]
        for data in invalid_data:
            response = self.client.post(self.url, data.write_only_payload())
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("user.views.send_verification_email.delay")
    @patch("user.views.UserSerializer.save_cached")
    def test_with_registered_user(self, mocked_cache, mocked_mail):
        mocked_cache.return_value = uuid.uuid4()
        mocked_mail.return_value = None

        payload = UserPayloadFactory().write_only_payload()
        User.objects.create(**payload)

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
