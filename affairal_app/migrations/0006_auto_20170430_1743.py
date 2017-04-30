# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('affairal_app', '0005_affairaluser_reg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='affairaluser',
            name='document',
            field=models.FileField(default=None, upload_to='documents/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='affairaluser',
            name='reg_id',
            field=models.TextField(default=uuid.UUID('b8b48ccb-a10b-435c-b339-f28788cb4bfe')),
        ),
    ]