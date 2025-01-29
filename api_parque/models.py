from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class TypeUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type_user = models.CharField(max_length=30)

    class Meta:
        db_table = 'type_user'

class TypeRegister(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type_register = models.CharField(max_length=30)

    class Meta:
        db_table = 'type_register'

class Status(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = 'status'

class User(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    type_id = models.ForeignKey(TypeUser, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'user'

class Register(models.Model):
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

    class Meta:
        db_table = 'register'

class Habitat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=50)
    register = models.ManyToManyField(Register, through='RegisterHabitat', related_name='habitats')

    class Meta:
        db_table = 'habitat'

class RegisterHabitat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'register_habitat'

class Threat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    register = models.ManyToManyField(Register, through='RegisterThreat', related_name='threats')

    class Meta:
        db_table = 'threat'

class RegisterThreat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    threat = models.ForeignKey(Threat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'register_threat'

class Sighting(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    description = models.TextField(max_length=300)
    date = models.DateField(auto_now=True)
    photo = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sighting'
