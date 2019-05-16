# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0011_receiveddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandlog',
            name='type_data',
            field=models.CharField(null=True, max_length=256, default=None),
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='type_data',
            field=models.CharField(null=True, max_length=256, default=None),
        ),
        migrations.AlterField(
            model_name='receiveddata',
            name='received_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
