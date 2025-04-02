from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, identifier, role, username, password, **extra_fields):
        user = self.model(identifier=identifier, password=password, role=role, username=username)
        user.save()

        return user

    def create_superuser(self, identifier, password):
        user = self.model(identifier=identifier, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()

        return user

class User(AbstractUser):
    identifier = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20)
    username = models.CharField(max_length=20, null=True) # change to be not required

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Vehicle(models.Model):
    number = models.CharField(max_length=7, unique=True)