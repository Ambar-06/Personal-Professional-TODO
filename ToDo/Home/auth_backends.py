from django.contrib.auth.backends import ModelBackend
from .models import *



class CustomUserBackend(ModelBackend):
    def authenticate(self, request, SignUpEmail=None, SignUpPassword=None, **kwargs):
        print(SignUpEmail)
        print(SignUpPassword)
        print('***********')
        print(UserSignUpModel.objects.get(SignUpEmail=SignUpEmail))
        try:
            user = UserSignUpModel.objects.get(SignUpEmail=SignUpEmail)
            print(user)
        except UserSignUpModel.DoesNotExist:
            return None
        if SignUpPassword == user.SignUpPassword:
            return user
        return None