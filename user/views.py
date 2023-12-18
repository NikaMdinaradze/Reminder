from .serializers import UserGetSerializer, UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.

class UserList(APIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserGetSerializer
        return UserCreateSerializer

    def post(self, request):
        user = request.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserDetail(APIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserGetSerializer
        return UserCreateSerializer

    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user)
        return Response(serializer.data)

    def put(self, request,pk):
        user = User.objects.get(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
