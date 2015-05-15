# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_tournament_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participation',
            options={'ordering': ['placement']},
        ),
        migrations.AlterModelOptions(
            name='tournament',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='player',
            name='max_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
