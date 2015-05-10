# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20150510_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participation',
            name='oowp',
        ),
        migrations.RemoveField(
            model_name='participation',
            name='owp',
        ),
    ]
