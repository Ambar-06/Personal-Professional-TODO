from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.http import JsonResponse
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
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import datetime

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
            request.session['loginemail'] = req_data['loginemail']
            request.session['loginpassword'] = req_data['loginpassword']
            return redirect(reverse("home"))

        return render(request, 'login.html')



def is_authenticated(request):
    loginemail = request.session.get('loginemail')
    loginpassword = request.session.get('loginpassword')

    # Check if a user with the provided email exists in the custom user model
    user_data = UserSignUpModel.objects.filter(SignUpEmail=loginemail).first()
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
    if request.method == 'GET':
        if is_authenticated(request):
            if loginemail:
                userData = UserSignUpModel.objects.filter(SignUpEmail=loginemail).first()
                userId = userData.UserUUID
                todaydate = datetime.datetime.now()
                todaydatestr = todaydate.strftime('%Y-%m-%d')
                threedaysafter = todaydate + datetime.timedelta(days=3)
                pending = []
                completed = []
                near = []
                today = []
                delayed = []
                taskslist = TasksModel.objects.filter(UserUUID=userId).order_by('-task_id')
                for task in taskslist:
                    taskDeadlinedate = task.TaskDeadline.strftime('%Y-%m-%d')
                    if task.IsCompleted == "True":
                        completed.append(task)
                    elif taskDeadlinedate == todaydatestr and task.IsCompleted != "True":
                        today.append(task)
                    elif datetime.datetime.strptime(taskDeadlinedate, "%Y-%m-%d") < datetime.datetime.strptime(todaydatestr, "%Y-%m-%d") and task.IsCompleted != "True":
                        delayed.append(task)
                    elif datetime.datetime.strptime(taskDeadlinedate, "%Y-%m-%d") < threedaysafter and task.IsCompleted != "True" and datetime.datetime.strptime(taskDeadlinedate, "%Y-%m-%d") != datetime.datetime.strptime(todaydatestr, "%Y-%m-%d"):
                        near.append(task)
                    elif task.IsCompleted != "True":
                        pending.append(task)
            today_json =  serializers.serialize('json', today)
            pending_json =  serializers.serialize('json', pending)
            near_json =  serializers.serialize('json', near)
            completed_json =  serializers.serialize('json', completed)
            delayed_json =  serializers.serialize('json', delayed)
            return render(request, 'home.html', {"Pending" : pending, "Near" : near, "Completed" : completed, "Delayed" : delayed, "Today" : today, "PendingJSON" : pending_json, "NearJSON" : near_json, "CompletedJSON" : completed_json, "DelayedJSON" : delayed_json, "TodayJSON" : today_json})
        messages.error(request, 'Session Expired, Please login again to continue.')
        return redirect(reverse("login"))
    if request.method == 'POST' and request.POST.get('methodtype') == 'post':
        req_data = {
            "TaskName" : request.POST.get('TaskName'),
            "TaskDeadline" : request.POST.get('TaskDeadline')
        }
        try:
            validated_data = TaskDataSchema(**req_data)
        except ValidationError as e:
            messages.error(request, f'{e.errors()}')
        
        userData = UserSignUpModel.objects.filter(SignUpEmail=request.session.get('loginemail')).first()
        taskData = TasksModel(
            UserUUID = userData.UserUUID,
            TaskName = validated_data.TaskName,
            TaskAddedOn = datetime.datetime.now(),
            TaskDeadline = validated_data.TaskDeadline,
            IsCompleted = 'False'
            )
        taskData.save()
        return HttpResponseRedirect(request.path_info)
    if request.method == 'POST' and request.POST.get('methodtype') == 'put':
        req_data = {
            "TaskName" : request.POST.get('UpdateTaskName'),
            "TaskDeadline" : request.POST.get('UpdateTaskDeadline')
        }
        try:
            validated_data = TaskDataSchema(**req_data)
        except ValidationError as e:
            messages.error(request, f'{e.errors()}')
        
        try:
            taskData = TasksModel.objects.get(task_id=request.POST.get('UpdateTaskId'))
        except TasksModel.DoesNotExist:
            pass
        else:
            taskData.TaskName = validated_data.TaskName
            taskData.TaskDeadline = validated_data.TaskDeadline
            taskData.save()
        return HttpResponseRedirect(request.path_info)



def logout_f(request):
    request.session.flush()
    return redirect('login')

@csrf_exempt
def mark_as_complete(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = TasksModel.objects.get(task_id=task_id)
        task.IsCompleted = 'True'
        task.save()
        return JsonResponse({'message': 'Task marked as complete'})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = TasksModel.objects.get(task_id=task_id)
        task.delete()
        return JsonResponse({'message': 'Task deleted'})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = TasksModel.objects.get(task_id=task_id)
        task.delete()
        return JsonResponse({'message': 'Task deleted'})
    return JsonResponse({'error': 'Invalid request method'})

def index(request):
    return render(request, 'index_home.html')