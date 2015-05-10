# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_player_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='default_password',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='awards',
            field=models.ManyToManyField(blank=True, to='backend.Award'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='staff',
            field=models.ManyToManyField(related_name='tournament_staff', blank=True, to='backend.Player'),
        ),
    ]
