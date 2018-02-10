# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20151008_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upfile',
            field=models.FileField(upload_to=b'documents/path'),
        ),
    ]
