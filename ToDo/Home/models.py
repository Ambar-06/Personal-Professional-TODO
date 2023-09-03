from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import uuid

# Create your models here.
class UserSignUpModel(models.Model):

    _id = models.AutoField(primary_key=True)
    UserUUID = models.UUIDField(default=uuid.uuid4, editable=False)
    SignUpName = models.CharField(max_length=255, blank=False, null=False)
    SignUpEmail = models.CharField(max_length=255, blank=False, null=False, unique=True)
    SignUpNumber = PhoneNumberField(null=False, blank=False, unique=True)
    SignUpPassword = models.CharField(max_length=500, blank=False, null=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.SignUpEmail)


class TasksModel(models.Model):

    task_id = models.AutoField(primary_key=True)
    UserUUID = models.CharField(max_length=255, blank=False, null=False)
    TaskName = models.CharField(max_length=255, blank=False, null=False)
    TaskAddedOn = models.DateTimeField()
    TaskDeadline = models.DateTimeField()
    IsCompleted = models.CharField(max_length=50, blank=False, null=False)