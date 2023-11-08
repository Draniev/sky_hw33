# Generated by Django 4.2.6 on 2023-11-08 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_tguser_auth_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tguser',
            name='auth_code',
        ),
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Код авторизации'),
        ),
    ]
