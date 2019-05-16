from django.db import models

import time
from django.forms.models import model_to_dict


def current():
    return float(time.time())


class Chip(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    mac = models.CharField(max_length=60)
    name = models.CharField(max_length=60, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)
    connection_exception = models.CharField(default=None, blank=True, null=True, max_length=500)


class RegisteredChip(Chip):
    pass

    def __str__(self):
        return u'%s %s %s' % (self.id, self.mac, self.name)

class DiscoveredChip(Chip):
    pass

    def __str__(self):
        return u'%s %s %s' % (self.id, self.mac, self.name)


class ChipCommand(models.Model):
    command = models.CharField(max_length=1)
    has_f = models.BooleanField(default=False)
    has_p = models.BooleanField(default=False)
    has_n = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    category = models.ForeignKey('CommandCategory')

    def image_tag2(self):
        return u'<img src="/static/frequ.png"/>'

    image_tag2.short_description = 'F P N'
    image_tag2.allow_tags = True

    def get_category_name(self):
        return self.category.name

    def __str__(self):
        return u'%s %s %s %s' % (self.id, self.command, self.name, self.category.name)


class CommandLog(models.Model):
    registered_chip = models.ForeignKey('RegisteredChip', related_name='registered_chips')
    command = models.ForeignKey('ChipCommand')
    send_date= models.DateTimeField(auto_now=True)
    successful = models.BooleanField(default=False)
    error = models.CharField(max_length=400, default=None, null=True, blank=True)
    send_index = models.PositiveIntegerField()
    scheduled = models.BooleanField(default=False)
    f = models.PositiveIntegerField(default=None, null=True)
    p = models.PositiveIntegerField(default=None, null=True)
    n = models.PositiveIntegerField(default=None, null=True)
    t_result = models.CharField(default=None, null=True, max_length=256)
    type_data = models.CharField(default=None, null=True, max_length=256)

    def __str__(self):
        return u'%s ' % model_to_dict(self)

class ReceivedData(models.Model):
    send_chip= models.ForeignKey('RegisteredChip', related_name='send_chip')
    received_time = models.DateTimeField(auto_now=True)
    t_result = models.CharField(default=None, null=True, max_length=256)
    type_data = models.CharField(default=None, null=True, max_length=256)

    def __str__(self):
        return u'%s ' % model_to_dict(self)

class CommandCategory(models.Model):
    index = models.PositiveIntegerField()
    name = models.CharField(max_length=60)

    def __str__(self):
        return u'%s %s index %s' % (self.id, self.name, self.index)


scheduled_command_type_choices = (
    ('once', 'once'),
    ('repeat', 'repeat'),
)

class ScheduledCommand(models.Model):
    registered_chip = models.ForeignKey('RegisteredChip', related_name='reg_chips')
    command = models.ForeignKey('ChipCommand', related_name='cmmds')
    # once or daily
    def image_tag(self):
        return u'<img src="/static/scheduling.png"/>'

    image_tag.short_description = 'Timing Scheduled Commands'
    image_tag.allow_tags = True

    execution_date_or_start_date = models.DateTimeField("Start Date")
    execution_end_date_if_repeating = models.DateTimeField("End Date", default=None, null=True, blank=True)
    seconds_between_executions = models.PositiveIntegerField("Session Time Period (T) in seconds:", default=0)
    send_turn_off_command_in_seconds = models.IntegerField("Session 'ON' time (t) in seconds", default=None, null=True, blank=True)
    type = models.CharField(max_length=15, default='once', choices=scheduled_command_type_choices)
    last_execution_log = models.ForeignKey('CommandLog', default=None, null=True, blank=True)
    retry_if_fails = models.BooleanField(default=False)
    name = models.CharField(default=None, null=False, blank=False, max_length=60)
    active = models.BooleanField(default=True)

    def image_tag2(self):
        return u'<img src="/static/frequ.png"/>'

    image_tag2.short_description = 'F P N'
    image_tag2.allow_tags = True

    f = models.PositiveIntegerField(default=None, null=True)
    p = models.PositiveIntegerField(default=None, null=True)
    n = models.PositiveIntegerField(default=None, null=True)





    def get_registered_chip(self):
        return self.registered_chip

    def get_command(self):
        return self.command

    def __str__(self):
        return u'Name: %s   Type:%s   Date:%s   Chip:%s   Command:%s' % (self.name, self.type, self.execution_date_or_start_date, self.registered_chip, self.command)



class TextBox(models.Model):
    text = models.CharField(default=None, null=True, blank=True, max_length=1000)

