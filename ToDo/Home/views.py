from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def test_f(request):
    json_data = {
        "status" : 200,
        "data" : '',
        "message" : 'Working well.',
    }
    return Response(json_data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def signup_f(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
