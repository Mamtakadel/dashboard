# Generated by Django 4.1 on 2024-04-24 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geospatial', '0007_alter_palikageometry_ward_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('temperature_2m', models.FloatField(blank=True, null=True)),
                ('precipitation_probability', models.FloatField(blank=True, null=True)),
                ('precipitation', models.FloatField(blank=True, null=True)),
                ('rain', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
