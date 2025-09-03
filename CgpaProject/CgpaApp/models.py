from django.db import models

# Create your models here.
class Register(models.Model):
    genders=[('Male','Male'),('Female','Female')]
    branches=[('CSE','CSE'),('ECE','ECE'),('IT','IT'),('EEE','EEE')]
    name=models.CharField(max_length=50)
    mobile_no=models.CharField(max_length=10)
    gender=models.CharField(max_length=10,choices=genders)
    branch=models.CharField(max_length=10,choices=branches)


