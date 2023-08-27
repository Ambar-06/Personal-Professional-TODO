from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from pydantic import ValidationError
from django.contrib import messages

import hashlib


from .schemas import *
from .models import *


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
    elif request.method == 'POST':
        try:
            try:
                validated_data = UserSignUpDataSchema(**request.data)
            except ValidationError as e:
                messages.error(request, 'Invalid Data, Please share valid data.')
                return render(request, 'signup.html')
            SignUpName = validated_data.signupname
            SignUpEmail = validated_data.signupemail
            SignUpNumber = validated_data.signupnumber
            SignUpPassword = validated_data.signuppassword
            SignUpConfirmPassword = validated_data.confirmpassword

            if SignUpPassword != SignUpConfirmPassword:
                messages.error(request, 'Password did not match.')
                return render(request, 'signup.html')
            
            password_encoded = SignUpPassword.encode() 

            password_hashed = hashlib.md5(password_encoded).hexdigest()
            
            UserData = UserSignUpModel(
                    SignUpName=SignUpName,
                    SignUpEmail=SignUpEmail,
                    SignUpNumber=SignUpNumber,
                    SignUpPassword=password_hashed
                )
            UserData.save()
            messages.success(request, 'Your email has been registered successfully. Login to continue')
            return render(request, 'signup.html')
        except Exception as e:
            print(e)
            return HttpResponse(f'<h1>{e}</h1>')


@api_view(['GET', 'POST'])
def login_f(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        return render(request, 'login.html')
