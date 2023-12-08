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


class Code(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    random_code = models.CharField(max_length=10, unique=True)
    used_by_user = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    redemption_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.random_code) + ' - ' + str(self.used_by_user)


class UserHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type_of_activity = models.CharField(max_length=50, choices=[('QR_SCAN', 'QR Scan')])
    accumulated_points = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user) + ' - ' + str(self.accumulated_points)
