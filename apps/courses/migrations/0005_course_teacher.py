# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 16:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_remove_teacher_course'),
        ('courses', '0004_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Teacher', verbose_name='\u6388\u8bfe\u6559\u5e08'),
        ),
    ]