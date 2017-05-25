# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-23 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_banner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('female', '\u5973'), ('male', '\u7537')], default='female', max_length=10, verbose_name='\u7528\u6237\u6027\u522b'),
        ),
    ]
