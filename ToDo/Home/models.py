from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import uuid

# Create your models here.
class UserSignUpModel(models.Model):

    _id = models.AutoField(primary_key=True)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    signup_name = models.CharField(max_length=255, blank=False, null=False)
    signup_email = models.CharField(max_length=255, blank=False, null=False, unique=True)
    signup_number = PhoneNumberField(null=True, unique=True)
    signup_password = models.CharField(max_length=500, blank=False, null=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.signup_email)


class TasksModel(models.Model):

    task_id = models.AutoField(primary_key=True)
    user_uuid = models.CharField(max_length=255, blank=False, null=False)
    task_name = models.CharField(max_length=255, blank=False, null=False)
    task_added_on = models.DateTimeField()
    task_deadline = models.DateTimeField()
    is_completed = models.CharField(max_length=50, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
