from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser, BaseModel):
    phone = PhoneNumberField(
        blank=True, 
        region='VN',
        help_text='Phone number format: +84xxxxxxxxx'
    )

    class Meta:
        db_table = 'users'
