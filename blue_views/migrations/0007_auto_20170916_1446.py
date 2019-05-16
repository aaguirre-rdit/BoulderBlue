# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0006_auto_20170723_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledcommand',
            name='execution_end_date_if_repeating',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='send_turn_off_command_in_seconds',
            field=models.IntegerField(null=True, default=None, blank=True),
        ),
    ]
