# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='user',
            field=models.ForeignKey(to='app.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tenant',
            field=models.ForeignKey(to='app.Tenant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userType',
            field=models.ForeignKey(to='app.User_Type'),
        ),
        migrations.AlterField(
            model_name='user_type',
            name='tenant',
            field=models.ForeignKey(to='app.Tenant'),
        ),
    ]
