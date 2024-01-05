from django.utils import timezone


class ToDoValidator:
    def __init__(self, title, todo, category, active, deadline):
        self.title = title
        self.todo = todo
        self.deadline = deadline
        self.active = active
        self.category = category
        self.errors = []

    def _check_deadline_with_current_time(self):
        """
        Check that the creation time is before the deadline.
        """
        if self.deadline < timezone.now():
            self.errors.append("deadline must be after current time")

    def _check_deadline_duration(self):
        """
        Check that the deadline is not more than ten years away.
        """
        if self.deadline > timezone.now() + timezone.timedelta(days=365 * 10):
            self.errors.append("The deadline cannot be longer than ten years")

    def _check_category_lowercase(self):
        """
        Check that the category is lowercase.
        """
        if not self.category.islower():
            self.errors.append("The category should be lowercase")

    def __call__(self, *args, **kwargs):
        self._check_deadline_duration()
        self._check_category_lowercase()
        self._check_deadline_with_current_time()
        return self.errors
