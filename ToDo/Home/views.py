from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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
        req_data = {
            'signupname':request.data.get('signupname'),
            'signupemail':request.data.get('signupemail'),
            'signupnumber': request.data.get('signupnumber'),
            'signuppassword': request.data.get('signuppassword'),
            'confirmpassword': request.data.get('confirmpassword')
        }
        if UserSignUpModel.objects.filter(SignUpEmail=request.data.get('signupemail')):
            messages.error(request, 'User already registered.')
            return render(request, 'signup.html')
        if UserSignUpModel.objects.filter(SignUpNumber=request.data.get('signupnumber')):
            messages.error(request, 'Number already registered.')
            return render(request, 'signup.html')
        try:
            try:
                validated_data = UserSignUpDataSchema(**req_data)
            except ValidationError as e:
                messages.error(request, f'{e.errors()}')
                return render(request, 'signup.html')
            SignUpName = validated_data.signupname
            SignUpEmail = validated_data.signupemail
            SignUpNumber = validated_data.signupnumber
            SignUpPassword = validated_data.signuppassword
            SignUpConfirmPassword = validated_data.confirmpassword

            if SignUpPassword != SignUpConfirmPassword:
                print('DID NOT MATCH')
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
            print('GOT IT')
            UserData.save()
            print('SAVED')
            messages.success(request, 'Your email has been registered successfully. Login to continue')
            return render(request, 'signup.html')
        except Exception as e:
            print(e)
            return HttpResponse(f'<h1>{e}</h1>')

def login_f(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        req_data = {
            'loginemail':request.data.get('loginemail'),
            'loginpassword': request.data.get('loginpassword')
        }

        if UserSignUpModel.objects.filter(SignUpEmail=request.data.get('loginemail')) == None or UserSignUpModel.objects.filter(SignUpEmail=request.data.get('loginemail')) == [] or UserSignUpModel.objects.filter(SignUpEmail=request.data.get('loginemail')) == '' or len(UserSignUpModel.objects.filter(SignUpEmail=request.data.get('loginemail'))) == 0:
            messages.error(request, 'User not found.')
            return render(request, 'login.html')
        try:
            validated_data = UserLoginDataSchema(**req_data)
        except ValidationError as e:
            messages.error(request, f'{e.errors()}')
            return render(request, 'login.html')
        Email = validated_data.loginemail
        Password = validated_data.loginpassword

        password_encoded = Password.encode()
        password_hashed = hashlib.md5(password_encoded).hexdigest()
        user = authenticate(request, SignUpEmail=Email, SignUpPassword=password_hashed)
        print(user, 'YEH HAI USER')
        if user is not None:
            print('TRUE')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password1111.')
            return redirect('login')
        

        
        # UserData = UserSignUpModel.objects.filter(SignUpEmail=request.data.get('loginemail')).first()
        # if password_hashed != UserData.SignUpPassword:
        #     messages.error(request, 'Invalid password.')
        #     return render(request, 'login.html')
        # else:
        #     return redirect('home', permanent=True)

        # return render(request, 'login.html')


# @api_view(['GET', 'POST'])
@login_required(login_url='login')
def home_f(request):
        return render(request, 'home.html')
    # if request.method == 'GET':
    #     return render(request, 'home.html')
    # return render(request, 'home.html')

@api_view(['POST'])
def logout_f(request):
    if 'is_authenticated' in request.session:
        del request.session['is_authenticated']
    return HttpResponse(status=200)