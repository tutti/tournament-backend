# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20150510_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
