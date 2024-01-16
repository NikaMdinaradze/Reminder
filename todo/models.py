from django.db import models

# Create your models here.


class ToDo(models.Model):
    title = models.CharField(max_length=100, null=False, default="")
    todo = models.CharField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField()
    active = models.BooleanField(default=True, null=False)
    category = models.CharField(max_length=255, default="")
    owner = models.ForeignKey(
        "auth.User", related_name="todos", on_delete=models.CASCADE, null=False
    )
    notified = models.BooleanField(default=False)
