# Generated by Django 5.1.3 on 2024-11-18 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='product',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='service',
        ),
        migrations.AddField(
            model_name='promotion',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='promotions', to='products.product'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='promotions', to='products.service'),
        ),
    ]
