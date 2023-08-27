from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.
class UserSignUpModel(models.Model):

    _id = models.AutoField(primary_key=True)
    UserUUID = models.UUIDField(max_length=500, blank=False, null=False)
    SignUpName = models.CharField(max_length=255, blank=False, null=False)
    SignUpEmail = models.CharField(max_length=255, blank=False, null=False, unique=True)
    SignUpNumber = PhoneNumberField(null=False, blank=False, unique=True)
    SignUpPassword = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return str(self.UserUUID)