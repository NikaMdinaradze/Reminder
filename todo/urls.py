from django.urls import path
from .views import ToDoList, ToDoDetail


urlpatterns = [
    path("", ToDoList.as_view(), name='todo-list'),
    path("<int:pk>", ToDoDetail.as_view(), name='todo-details'),
    ]