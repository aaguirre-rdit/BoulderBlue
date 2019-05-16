# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0007_auto_20170916_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledcommand',
            name='name',
            field=models.CharField(default=None, max_length=60),
        ),
    ]
