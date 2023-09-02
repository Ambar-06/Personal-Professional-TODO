from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from pydantic import ValidationError
from django.contrib import messages
from django.urls import reverse

import hashlib


from .schemas import *
from .models import *


# Create your views here.

def signup_f(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        req_data = {
            'signupname':request.POST.get('signupname'),
            'signupemail':request.POST.get('signupemail'),
            'signupnumber': request.POST.get('signupnumber'),
            'signuppassword': request.POST.get('signuppassword'),
            'confirmpassword': request.POST.get('confirmpassword')
        }
        if UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('signupemail')):
            messages.error(request, 'User already registered.')
            return render(request, 'signup.html')
        if UserSignUpModel.objects.filter(SignUpNumber=request.POST.get('signupnumber')):
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

@cache_control(no_cache=True, must_revalidate=True)
def login_f(request):
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'login.html')
    elif request.method == 'POST':
        req_data = {
            'loginemail':request.POST.get('loginemail'),
            'loginpassword': request.POST.get('loginpassword')
        }

        if UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('loginemail')) == None or UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('loginemail')) == [] or UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('loginemail')) == '' or len(UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('loginemail'))) == 0:
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

        UserData = UserSignUpModel.objects.filter(SignUpEmail=request.POST.get('loginemail')).first()
        if password_hashed != UserData.SignUpPassword:
            messages.error(request, 'Invalid password.')
            return render(request, 'login.html')
        else:
            print(request.POST.get('loginemail'), "THEEEK PEHLE")
            request.session['loginemail'] = req_data['loginemail']
            request.session['loginpassword'] = req_data['loginpassword']
            return redirect(reverse("home"))

        return render(request, 'login.html')



def is_authenticated(request):
    loginemail = request.session.get('loginemail')
    loginpassword = request.session.get('loginpassword')

    # Check if a user with the provided email exists in the custom user model
    user_data = UserSignUpModel.objects.filter(SignUpEmail=loginemail).first()
    print(user_data)
    if user_data is None:
        # User with the provided email doesn't exist
        return False

    # Hash the provided password and compare it with the stored hashed password
    password_encoded = loginpassword.encode()
    password_hashed = hashlib.md5(password_encoded).hexdigest()

    if password_hashed != user_data.SignUpPassword:
        # Invalid password
        return False

    # Authentication succeeded
    return True


@cache_control(no_cache=True, must_revalidate=True)
def home_f(request):
    # Retrieve data from the session
    loginemail = request.session.get('loginemail')
    loginpassword = request.session.get('loginpassword')
    print(loginemail)
    print(request.method)
    if request.method == 'GET':
        print('YES')
        print(request)
        if is_authenticated(request):
            if loginemail:
                print(loginemail, 'INSIDE HOME')  # Print the loginemail
            return render(request, 'home.html')
        messages.error(request, 'Session Expired, Please login again to continue.')
        return redirect(reverse("login"))


def logout_f(request):
    if 'is_authenticated' in request.session:
        del request.session['is_authenticated']
    return HttpResponse(status=200)