# Generated by Django 2.2.16 on 2020-09-23 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='stock',
            constraint=models.UniqueConstraint(fields=('author', 'code'), name='stock_code_booking'),
        ),
    ]
