from .serializers import ToDoSerializer
from .models import ToDo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.


class ToDoList(APIView):

    serializer_class = ToDoSerializer
    def get(self, request):
        snippets = ToDo.objects.all()
        serializer = self.serializer_class(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        snippet = request.data
        serializer = self.serializer_class(data=snippet)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetail(APIView):
    serializer_class = ToDoSerializer

    def get_object(self, pk):
        try:
            return ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Http404

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo, data=request)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status.HTTP_204_NO_CONTENT)

