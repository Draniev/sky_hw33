# Generated by Django 4.2.6 on 2023-10-30 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0004_alter_goal_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='Дата создания')),
                ('updated', models.DateTimeField(verbose_name='Дата последнего обновления')),
                ('text', models.CharField(max_length=255, verbose_name='Текст')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goals.goal', verbose_name='Цель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
