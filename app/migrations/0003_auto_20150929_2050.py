# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20150929_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_More',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tenant', models.ForeignKey(to='app.Tenant')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='tenant',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userType',
        ),
        migrations.AlterField(
            model_name='file',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='user_more',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_more',
            name='userType',
            field=models.ForeignKey(to='app.User_Type'),
        ),
    ]
