# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avatar',
            old_name='image',
            new_name='image_male',
        ),
        migrations.RenameField(
            model_name='avatar',
            old_name='name',
            new_name='name_male',
        ),
        migrations.AddField(
            model_name='avatar',
            name='image_female',
            field=models.ImageField(upload_to='', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='avatar',
            name='name_female',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
