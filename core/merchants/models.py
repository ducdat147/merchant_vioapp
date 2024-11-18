from django.db import models
from django.conf import settings
from core.models import BaseModel


class Merchant(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='merchants/logos/', blank=True)
    address = models.TextField()

    class Meta:
        db_table = 'merchants'

    def __str__(self):
        return self.name
