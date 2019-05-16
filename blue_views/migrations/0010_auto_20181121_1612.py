# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0009_textbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandlog',
            name='t_result',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='scheduledcommand',
            name='execution_date_or_start_date',
            field=models.DateTimeField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='scheduledcommand',
            name='execution_end_date_if_repeating',
            field=models.DateTimeField(verbose_name='End Date', default=None, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scheduledcommand',
            name='seconds_between_executions',
            field=models.PositiveIntegerField(verbose_name='Session Time Period (T) in seconds:', default=0),
        ),
        migrations.AlterField(
            model_name='scheduledcommand',
            name='send_turn_off_command_in_seconds',
            field=models.IntegerField(verbose_name="Session 'ON' time (t) in seconds", default=None, blank=True, null=True),
        ),
    ]
