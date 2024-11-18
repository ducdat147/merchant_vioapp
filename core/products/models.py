from django.db import models
from core.models import BaseModel
from django.core.exceptions import ValidationError


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Hashtag(BaseModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'hashtags'

    def __str__(self):
        return f'#{self.name}'


class Keyword(BaseModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'keywords'

    def __str__(self):
        return self.name


class Product(BaseModel):
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/')
    categories = models.ManyToManyField(Category)
    hashtags = models.ManyToManyField(Hashtag)
    keywords = models.ManyToManyField(Keyword)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f'{self.name} - {self.merchant.name}'


class Service(BaseModel):
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)
    hashtags = models.ManyToManyField(Hashtag)
    keywords = models.ManyToManyField(Keyword)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f'{self.name} - {self.merchant.name}'


class Promotion(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)
    services = models.ManyToManyField(Service, related_name='promotions', blank=True)

    class Meta:
        db_table = 'promotions'
        
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be after start date')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.discount_percent}%)'
