from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from todo.models import ToDo

# Create your tests here.

TODO_VALID_DATA = {
    "title": "Test ToDo",
    "todo": "This is a test ToDo",
    "created": timezone.now(),
    "deadline": timezone.now() + timezone.timedelta(days=1),
}
TODO_INVALID_DATA = {
    "title": "Test ToDo",
    "todo": "This is a test ToDo",
    "created": timezone.now(),
    "deadline": timezone.now() - timezone.timedelta(days=1),
}


class ToDoModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a ToDo instance for testing
        self.todo = ToDo.objects.create(
            **TODO_VALID_DATA,
            owner=self.user,
        )

    def test_todo_creation(self):
        """
        Test if a ToDo instance is created correctly.
        """
        self.assertEqual(self.todo.title, "Test ToDo")
        self.assertEqual(self.todo.todo, "This is a test ToDo")
        self.assertIsNotNone(self.todo.created)
        self.assertIsNotNone(self.todo.deadline)
        self.assertEqual(self.todo.owner, self.user)

    def test_todo_update(self):
        """
        Test updating a ToDo instance.
        """
        new_title = "Updated ToDo Title"
        new_todo_content = "This ToDo has been updated."
        new_deadline = timezone.now() + timezone.timedelta(days=14)

        self.todo.title = new_title
        self.todo.todo = new_todo_content
        self.todo.deadline = new_deadline
        self.todo.save()

        updated_todo = ToDo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, new_title)
        self.assertEqual(updated_todo.todo, new_todo_content)
