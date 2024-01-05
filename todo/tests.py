from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from todo.models import ToDo
from todo.serializers import ToDoSerializer

# Create your tests here.
TODO_WITHOUT_DEFAULTS = {
    "todo": "This is a test ToDo",
    "deadline": timezone.now() + timezone.timedelta(days=1),
}

TODO_VALID_DATA = {
    **TODO_WITHOUT_DEFAULTS,
    "title": "Test ToDo",
    "created": timezone.now(),
    "active": True,
    "category": "testing",
}
TODO_INVALID_DATA = {
    **TODO_WITHOUT_DEFAULTS,
    "title": "Test ToDo",
    "created": timezone.now(),
    "deadline": timezone.now() - timezone.timedelta(days=1),
    "category": "testing",
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
        self.assertTrue(self.todo.active)
        self.assertEqual(self.todo.category, "testing")

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

    def test_defaults(self):
        """
        Test Default Values
        """
        todo_defaults = ToDo.objects.create(**TODO_WITHOUT_DEFAULTS, owner=self.user)

        self.assertEqual(todo_defaults.title, "")
        self.assertTrue(todo_defaults.active)
        self.assertEqual(todo_defaults.category, "")


class ToDoSerializerTests(TestCase):
    def test_valid_todo_serializer(self):
        valid_data = TODO_VALID_DATA

        serializer = ToDoSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_todo_serializer(self):
        invalid_data = {
            "title": "Invalid ToDo",
            "todo": "This is an invalid ToDo",
            "category": "InvalidCategory",
            "active": True,
            "deadline": timezone.now() - timezone.timedelta(days=7),
        }

        serializer = ToDoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "deadline must be after current time", serializer.errors["non_field_errors"]
        )
        self.assertIn(
            "The category should be lowercase", serializer.errors["non_field_errors"]
        )

    def test_valid_todo_serializer_with_long_deadline(self):
        valid_data = {
            "title": "Complete Assignment",
            "todo": "Finish the coding assignment",
            "category": "personal",
            "active": True,
            "deadline": timezone.now() + timezone.timedelta(days=365 * 9),
        }

        serializer = ToDoSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_todo_serializer_with_long_deadline(self):
        invalid_data = {
            "title": "Invalid ToDo",
            "todo": "This is an invalid ToDo",
            "category": "personal",
            "active": True,
            "deadline": timezone.now() + timezone.timedelta(days=365 * 11),
        }

        serializer = ToDoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "The deadline cannot be longer than ten years",
            serializer.errors["non_field_errors"],
        )
