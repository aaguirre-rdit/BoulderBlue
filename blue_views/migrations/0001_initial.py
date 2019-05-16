# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True)),
                ('mac', models.CharField(max_length=60)),
                ('name', models.CharField(default=None, blank=True, max_length=60, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChipStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.TextField(blank=True, default=None, null=True)),
                ('set_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscoveredChip',
            fields=[
                ('chip_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='blue_views.Chip', serialize=False)),
            ],
            bases=('blue_views.chip',),
        ),
        migrations.CreateModel(
            name='RegisteredChip',
            fields=[
                ('chip_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='blue_views.Chip', serialize=False)),
            ],
            bases=('blue_views.chip',),
        ),
        migrations.AddField(
            model_name='chipstatus',
            name='registered_chip',
            field=models.ForeignKey(related_name='registered_chips', to='blue_views.RegisteredChip'),
        ),
    ]
