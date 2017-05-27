from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    password = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=15)
    isAdmin = models.BooleanField(default=False)