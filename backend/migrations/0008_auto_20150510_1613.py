# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20150510_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='oowp',
            field=models.DecimalField(max_digits=5, default=0, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participation',
            name='owp',
            field=models.DecimalField(max_digits=5, default=0, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(through='backend.Participation', to='backend.Player', blank=True, related_name='tournament_players'),
        ),
    ]
