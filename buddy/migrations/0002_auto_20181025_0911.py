# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buddy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mygym',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mygym', to='buddy.Gym'),
        ),
    ]
