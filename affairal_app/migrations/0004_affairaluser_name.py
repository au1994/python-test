# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affairal_app', '0003_auto_20170430_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='affairaluser',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
