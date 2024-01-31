from django.contrib.auth.models import User
from factory import Faker
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    password = Faker("password")


class UserPayloadFactory:
    """Factory class that creates payloads for user endpoints"""

    def __init__(
        self,
        username="string",
        password="string",
        email="user@example.com",
        first_name="string",
        last_name="string",
    ):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def write_only_payload(self):
        payload = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        return payload

    def read_only_payload(self):
        payload = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        return payload
