from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=2000)
    description = models.CharField(max_length=500)


    def __str__(self):
        return str(self.title)
    

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    due = models.DateField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subject)    


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)       
