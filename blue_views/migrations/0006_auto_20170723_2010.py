# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0005_auto_20170723_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledcommand',
            name='f',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='n',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='p',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='seconds_between_executions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scheduledcommand',
            name='type',
            field=models.CharField(max_length=15, choices=[('once', 'once'), ('repeat', 'repeat')], default='once'),
        ),
    ]
