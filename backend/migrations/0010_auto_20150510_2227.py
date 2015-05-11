# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20150510_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(related_name='game_p2', null=True, blank=True, to='backend.Player'),
        ),
    ]
