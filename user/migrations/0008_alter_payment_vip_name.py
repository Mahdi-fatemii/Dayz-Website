# Generated by Django 5.0.1 on 2024-01-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='vip_name',
            field=models.CharField(default='Normal', max_length=100),
        ),
    ]
