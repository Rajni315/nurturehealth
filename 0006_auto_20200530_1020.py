# Generated by Django 3.0.4 on 2020-05-30 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NurtureHealthApp', '0005_auto_20200529_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='add_treatment',
            options={},
        ),
        
    ]