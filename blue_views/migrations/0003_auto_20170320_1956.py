# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0002_auto_20170129_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledCommand',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('execution_date_or_start_date', models.DateTimeField()),
                ('type', models.CharField(max_length=15, default='once', choices=[('once', 'once'), ('daily', 'daily')])),
                ('retry_if_fails', models.BooleanField(default=False)),
                ('name', models.CharField(null=True, max_length=60, default=None, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('command', models.ForeignKey(to='blue_views.ChipCommand', related_name='cmmds')),
            ],
        ),
        migrations.AddField(
            model_name='commandlog',
            name='scheduled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='last_execution_log',
            field=models.ForeignKey(to='blue_views.CommandLog', blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='scheduledcommand',
            name='registered_chip',
            field=models.ForeignKey(to='blue_views.RegisteredChip', related_name='reg_chips'),
        ),
    ]
