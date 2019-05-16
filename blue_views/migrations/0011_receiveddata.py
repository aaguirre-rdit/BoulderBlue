# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0010_auto_20181121_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('received_time', models.PositiveIntegerField()),
                ('t_result', models.CharField(null=True, max_length=256, default=None)),
                ('send_chip', models.ForeignKey(related_name='send_chip', to='blue_views.RegisteredChip')),
            ],
        ),
    ]
