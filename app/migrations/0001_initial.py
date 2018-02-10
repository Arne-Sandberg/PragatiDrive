# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('filepath', models.FilePathField(max_length=1000)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('filesize', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('space', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, serialize=False, primary_key=True)),
                ('tenant', models.OneToOneField(to='app.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='User_Type',
            fields=[
                ('uTypeId', models.AutoField(serialize=False, primary_key=True)),
                ('userType', models.CharField(max_length=1)),
                ('maxStorage', models.CharField(max_length=6)),
                ('allowedExt', models.CharField(max_length=150)),
                ('maxSize', models.CharField(max_length=6)),
                ('tenant', models.OneToOneField(to='app.Tenant')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userType',
            field=models.OneToOneField(to='app.User_Type'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.OneToOneField(to='app.User'),
        ),
    ]
