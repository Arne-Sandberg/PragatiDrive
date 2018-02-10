# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151008_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upfile',
            field=models.FileField(upload_to=b'documents/user.username'),
        ),
    ]
