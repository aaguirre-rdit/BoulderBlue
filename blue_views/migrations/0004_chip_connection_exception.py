# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0003_auto_20170320_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='chip',
            name='connection_exception',
            field=models.CharField(blank=True, max_length=500, null=True, default=None),
        ),
    ]
