from django.db import models
from accounts.models import User


class Password(models.Model):
    url = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner')
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class SharePassword(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='user', null=True)
    password = models.ForeignKey(Password, on_delete=models.CASCADE)
    view = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
