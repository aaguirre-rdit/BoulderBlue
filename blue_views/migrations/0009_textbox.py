# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0008_auto_20180928_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.CharField(max_length=1000, null=True, blank=True, default=None)),
            ],
        ),
    ]
