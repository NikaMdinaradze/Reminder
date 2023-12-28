from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ToDo
from .permissions import IsOwner
from .serializers import ToDoSerializer

# Create your views here.


class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ToDoSerializer

    def get(self, request):
        """Gets Authenticated User's ToDos"""
        todo = ToDo.objects.filter(owner=request.user)
        serializer = self.serializer_class(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Creates ToDo"""
        todo = request.data
        serializer = self.serializer_class(data=todo)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetail(APIView):
    permission_classes = [IsOwner]
    serializer_class = ToDoSerializer

    def get_object(self, pk):  # noqa
        try:
            obj = ToDo.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except ToDo.DoesNotExist:
            raise Http404()

    def put(self, request, pk):
        """Updates User's ToDo with Id"""
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """Deletes User's ToDo with Id"""
        todo = self.get_object(pk)
        todo.delete()
        return Response(status.HTTP_204_NO_CONTENT)
