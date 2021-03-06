# Generated by Django 2.2.10 on 2020-02-16 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import photobook.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photobook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('thumbnail', models.ImageField(upload_to=photobook.models.Photobook.date_upload_to)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=photobook.models.Images.date_upload_to)),
                ('photobook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photobook.Photobook')),
            ],
        ),
    ]
