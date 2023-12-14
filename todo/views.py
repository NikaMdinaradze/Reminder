from .serializers import ToDoSerializer
from .models import ToDo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.


class ToDoList(APIView):
    def get(self, request):
        snippets = ToDo.objects.all()
        serializer = ToDoSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        snippet = request.data
        serializer = ToDoSerializer(data=snippet)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToDoDetail(APIView):

    def get_object(self, pk):
        try:
            return ToDo.object.get(pk=pk)
        except ToDo.DoesNotExist:
            return Http404

