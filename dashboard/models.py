from datetime import datetime
from django.db import models

class Profile(models.Model):
    nom = models.CharField(max_length=32)
    prenom = models.CharField(max_length=32)
    sexe =  models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    ville = models.CharField(max_length=32)
    contact = models.CharField(max_length=32)
    create_at = models.DateTimeField(default=datetime.now, blank=True)
    
    
class User(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  
class Data(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()   
    classe = models.CharField(max_length=32)
    predict = models.FloatField()  
    create_at = models.DateTimeField(default=datetime.now, blank=True)  