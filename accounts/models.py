from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    experience_points = models.IntegerField(default=0)
