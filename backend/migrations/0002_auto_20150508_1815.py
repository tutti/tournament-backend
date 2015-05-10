# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='awards',
            field=models.ManyToManyField(to='backend.Award'),
        ),
    ]
