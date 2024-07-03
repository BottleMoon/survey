from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.TextField()
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    # job = models.TextField()


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=128, unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

