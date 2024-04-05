# Create your models here.
from django.db import models

class UserAuth(models.Model):
    username=models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email=models.EmailField(blank=True,null=True) 
    firstname=models.CharField(max_length=200, null=True, blank=True) 
    lastname=models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username