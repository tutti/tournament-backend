# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20150510_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='avatar',
            field=models.ForeignKey(default='', to='backend.Avatar'),
            preserve_default=False,
        ),
    ]
