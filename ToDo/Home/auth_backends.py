from django.contrib.auth.backends import ModelBackend
from .models import *



class CustomUserBackend(ModelBackend):
    def authenticate(self, request, SignUpEmail=None, SignUpPassword=None, **kwargs):
        try:
            user = UserSignUpModel.objects.get(signup_email=SignUpEmail)
        except UserSignUpModel.DoesNotExist:
            return None
        if SignUpPassword == user.signup_password:
            return user
        return None