from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    experience_points = models.IntegerField(default=0)


class Ranking(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()
    from_points = models.PositiveIntegerField()
    to_points = models.PositiveIntegerField()
    image = models.ImageField(upload_to='rankings_images/', blank=True, null=True)

    def __str__(self):
        return str(self.level) + ' - ' + self.name
