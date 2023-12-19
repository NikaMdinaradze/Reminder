from django.urls import path
from .views import Register, UserMe


urlpatterns = [
    path("", Register.as_view(), name='user-register'),
    path("me/", UserMe.as_view(), name='user-details'),
    ]