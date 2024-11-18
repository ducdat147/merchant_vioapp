from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel


class User(AbstractUser, BaseModel):
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = 'users'
