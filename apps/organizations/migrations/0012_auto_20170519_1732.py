# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-19 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='learn_what',
            field=models.CharField(default='', max_length=200, verbose_name='\u80fd\u5b66\u5230\u4ec0\u4e48'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='need_know',
            field=models.CharField(default='', max_length=200, verbose_name='\u8bfe\u7a0b\u987b\u77e5'),
        ),
    ]
