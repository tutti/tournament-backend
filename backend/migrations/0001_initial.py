# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('winner', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('placement', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('owp', models.DecimalField(max_digits=5, decimal_places=2)),
                ('oowp', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('pop_id', models.IntegerField(primary_key=True, serialize=False)),
                ('gender', models.CharField(default='M', max_length=1)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('roundnum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('xml', models.TextField()),
                ('players', models.ManyToManyField(related_name='tournament_players', through='backend.Participation', to='backend.Player')),
                ('staff', models.ManyToManyField(related_name='tournament_staff', to='backend.Player')),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(to='backend.Tournament'),
        ),
        migrations.AddField(
            model_name='participation',
            name='player',
            field=models.ForeignKey(to='backend.Player'),
        ),
        migrations.AddField(
            model_name='participation',
            name='tournament',
            field=models.ForeignKey(to='backend.Tournament'),
        ),
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(related_name='game_p1', to='backend.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(related_name='game_p2', to='backend.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.ForeignKey(to='backend.Round'),
        ),
    ]
