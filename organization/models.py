from django.db import models
from accounts.models import User


class Organization(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Members(models.Model):
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AddOrganizationPasswords(models.Model):
    url = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)



