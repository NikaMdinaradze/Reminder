from django.db import models

# Create your models here.


class ToDo(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    todo = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
