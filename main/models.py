from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, identifier, role, username, password, **extra_fields):
        user = self.model(identifier=identifier, role=role, username=username)
        user.set_password(password)
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

    def __str__(self) -> str:
        return f'{self.identifier} {self.username} {self.role}'

class Vehicle(models.Model):
    number = models.CharField(max_length=7, unique=True)

class PassageLog(models.Model):
    class Meta:
        db_table = 'passage_log'

class ParkingSpot(models.Model):
    spot_number = models.IntegerField(unique=True)
    district = models.CharField(max_length=20)

    class Meta: 
        db_table = 'parking_spot'

    def __str__(self) -> str:
        return f'{self.spot_number} {self.district}'

class ParkingSpotReservation(models.Model):
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.RESTRICT)
    reserved_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'parking_spot_reservation'