# Generated by Django 2.2.10 on 2020-02-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='body',
            field=models.TextField(verbose_name='내용'),
        ),
    ]
