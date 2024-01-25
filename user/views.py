from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import Http404
from django.urls import reverse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.tasks import send_verification_email

from .serializers import UserSerializer


# Create your views here.
class Register(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        """Request User  Creation(Registration)"""
        user = request.data
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        key = serializer.save_cached()
        site_url = get_current_site(request)
        url = f"{site_url}{reverse('user-register')}?code={key}"
        send_verification_email.delay(user["email"], url)
        return Response("Verify from Email", status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="code", description="Email code", type=str),
        ],
    )
    def get(self, request):
        """Verify User"""
        code = request.query_params.get("code", None)
        if code is None:
            return Response(
                {"error": "Code parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = cache.get(code)
        if user is None:
            return Response(
                {"error": "User not found for the given code or it is expired."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserSerializer

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
