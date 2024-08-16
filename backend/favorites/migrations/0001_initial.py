# Generated by Django 5.0.6 on 2024-08-16 00:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
            ],
        ),
    ]
