# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 14:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_teacher_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='course',
        ),
    ]