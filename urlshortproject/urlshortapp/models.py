from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Urls(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_link",default=1, null=True)   
    userLink = models.CharField(max_length=10000)
    uuid = models.CharField(max_length=20)