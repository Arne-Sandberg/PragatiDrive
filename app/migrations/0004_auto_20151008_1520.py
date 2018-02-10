# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150929_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='file',
            name='filepath',
        ),
        migrations.RemoveField(
            model_name='file',
            name='filesize',
        ),
        migrations.AddField(
            model_name='file',
            name='upfile',
            field=models.FileField(default='', upload_to=b'documents/'),
            preserve_default=False,
        ),
    ]
