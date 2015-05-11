# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20150510_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(to='backend.Player', related_name='game_p2', blank=True),
        ),
    ]
