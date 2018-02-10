# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20151008_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upfile',
            field=models.FileField(upload_to=app.models.upload_file),
        ),
    ]
