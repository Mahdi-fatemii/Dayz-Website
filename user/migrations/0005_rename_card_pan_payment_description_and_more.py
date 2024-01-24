# Generated by Django 5.0.1 on 2024-01-24 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='card_pan',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='ref_id',
            new_name='vip_name',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='token',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]
