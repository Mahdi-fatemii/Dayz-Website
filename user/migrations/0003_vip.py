# Generated by Django 5.0.1 on 2024-01-23 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_viplevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_name', models.CharField(max_length=100)),
                ('vip_description', models.CharField(max_length=300)),
                ('vip_price', models.FloatField()),
            ],
        ),
    ]
