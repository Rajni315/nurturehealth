# Generated by Django 3.0.4 on 2020-05-30 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NurtureHealthApp', '0007_auto_20200530_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('disease', models.CharField(blank=True, max_length=250, null=True)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(max_length=100)),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NurtureHealthApp.Department')),
                ('doctor', models.ForeignKey(limit_choices_to={'is_staff': True, 'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(limit_choices_to={'is_staff': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Appointments',
            },
        ),
        migrations.CreateModel(
            name='Rev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='NurtureHealthApp.Appoint')),
                ('doctor', models.ForeignKey(limit_choices_to={'is_staff': True, 'is_superuser': False}, on_delete=django.db.models.deletion.CASCADE, related_name='review_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(limit_choices_to={'is_staff': False}, on_delete=django.db.models.deletion.CASCADE, related_name='review_patient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
    ]