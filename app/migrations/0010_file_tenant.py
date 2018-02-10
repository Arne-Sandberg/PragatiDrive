# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20151009_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='tenant',
            field=models.ForeignKey(default=1, to='app.Tenant'),
            preserve_default=False,
        ),
    ]
