# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_views', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChipCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('command', models.CharField(max_length=1)),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='CommandCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('index', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='CommandLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('send_date', models.DateTimeField(auto_now=True)),
                ('successful', models.BooleanField(default=False)),
                ('error', models.CharField(null=True, default=None, max_length=400, blank=True)),
                ('send_index', models.PositiveIntegerField()),
                ('command', models.ForeignKey(to='blue_views.ChipCommand')),
                ('registered_chip', models.ForeignKey(to='blue_views.RegisteredChip', related_name='registered_chips')),
            ],
        ),
        migrations.RemoveField(
            model_name='chipstatus',
            name='registered_chip',
        ),
        migrations.DeleteModel(
            name='ChipStatus',
        ),
        migrations.AddField(
            model_name='chipcommand',
            name='category',
            field=models.ForeignKey(to='blue_views.CommandCategory'),
        ),
    ]
