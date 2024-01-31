import re


class UserValidator:
    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.errors = []

    def _check_password(self):
        if len(self.password) >= 8:
            self.errors.append("Password must be at least 8 characters")

    def _check_email(self):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        match = re.match(pattern, self.email)
        if bool(match):
            self.errors.append("Invalid email")

    def _check_first_name(self):
        if len(self.first_name) <= 0:
            self.errors.append("Invalid first name")

    def _check_last_name(self):
        if len(self.first_name) <= 0:
            self.errors.append("Invalid last name")

    def perform_check(self):
        self._check_password()
        self._check_email()
        self._check_first_name()
        self._check_last_name()
        return self.errors
