from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(default='Custom', max_length=100)
    age = models.IntegerField(default=0)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username}'
