# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 14:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_org',
        ),
    ]