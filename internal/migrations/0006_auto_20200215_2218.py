# Generated by Django 2.2.10 on 2020-02-15 13:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0005_auto_20200215_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, related_name='like_user_set', through='internal.Like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='제목'),
        ),
    ]