from django.db import models

# Create your models here.
class TypeUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type_user = models.CharField(max_length=30)

class TypeRegister(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type_register = models.CharField(max_length=30)

class Status(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    status = models.CharField(max_length=30)

class User(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    type_id = models.ForeignKey(TypeUser, on_delete=models.CASCADE)

class Register(models.Mode):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    habitat = models.CharField(max_length=100)
    distribution = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    type_id = models.ForeignKey(TypeRegister, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)


class Sithing(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    description = models.TextField(max_length=300)
    date = models.DateField(auto_now=True)
    photo = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
