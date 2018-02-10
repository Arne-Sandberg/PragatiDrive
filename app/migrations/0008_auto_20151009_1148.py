# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20151009_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upfile',
            field=models.FileField(upload_to=b'documents<function upload_file at 0x03247F70>'),
        ),
    ]
