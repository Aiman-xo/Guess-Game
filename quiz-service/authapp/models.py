from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MainUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    class Meta:
        verbose_name = 'Main User'
        verbose_name_plural = 'Main Users'