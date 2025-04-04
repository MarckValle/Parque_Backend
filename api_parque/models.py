from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    status = models.CharField(max_length=100)
    
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
        db_table = 'user_park'

class Register(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    function = models.CharField(max_length=300)
    description = models.CharField(max_length=200)
    habitat = models.CharField(max_length=100)
    distribution = models.CharField(max_length=100)
    sound = models.CharField(max_length=300)
    photo = models.CharField(max_length=300)
    video = models.CharField(max_length=300)
    type_id = models.ForeignKey(TypeRegister, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)


    class Meta:
        db_table = 'register'

class Habitat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    description = models.CharField(max_length=300)
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=300)
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
    photo = models.CharField(max_length=300)
    type_register = models.ForeignKey(TypeRegister, on_delete=models.CASCADE)
    sighting_name = models.ForeignKey(Register, on_delete=models.CASCADE)
    full_name = models.TextField(max_length=300)
    validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'sighting'

class Alimentation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=300)
    alimentation = models.ManyToManyField(Register, through='RegisterAlimentation', related_name='alimentations')

    class Meta:
        db_table = 'alimentation'

class RegisterAlimentation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    alimentation = models.ForeignKey(Alimentation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'register_alimentation'

class Distribution(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=300)
    distribution = models.ManyToManyField(Register, through='RegisterDistribution', related_name='distributions')

    class Meta:
        db_table = 'distribution'

class RegisterDistribution(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)

    class Meta:
        db_table = 'register_distribution'

class Comments(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    type_comment = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    class Meta:
        db_table = 'comments'

class PageVisit(models.Model):
    path = models.CharField(max_length=256)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    user = models.ForeignKey('api_parque.User', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'page_visit'
        indexes = [
            models.Index(fields=['path']),
            models.Index(fields=['timestamp']),
        ]
