from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserGetSerializer


# Create your views here.
class Register(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        """Creates User (Registration)"""
        user = request.data
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserGetSerializer
        return UserCreateSerializer

    @staticmethod
    def get_user(request):
        user = request.user
        if user.is_authenticated:
            return user
        else:
            raise Http404("User not found or not logged in")

    def get(self, request):
        """Gets Authenticated User's Info"""
        user = self.get_user(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user)
        return Response(serializer.data)

    def put(self, request):
        """Updates Authenticated User's Info"""
        user = self.get_user(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        """Deletes Authenticated User's Info"""
        user = self.get_user(request)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
