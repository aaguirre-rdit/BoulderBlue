# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0004_chip_connection_exception'),
    ]

    operations = [
        migrations.AddField(
            model_name='chipcommand',
            name='has_f',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chipcommand',
            name='has_n',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chipcommand',
            name='has_p',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commandlog',
            name='f',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='commandlog',
            name='n',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='commandlog',
            name='p',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='chipcommand',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
