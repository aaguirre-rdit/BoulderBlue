from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from itertools import groupby
from django.forms.models import model_to_dict
from django.db import transaction
from operator import itemgetter

from threading import Timer as ThreadTimer


from BoulderBlueServerWebApp.BoulderBlueServerWebApp import settings
from BoulderBlueServerWebApp.blue_views.models import *

import datetime
from django.utils import timezone


def run_scheduled_commands_if_necessary():
    now = timezone.now()
    # print("\n\n\n run_scheduled_commands_if_necessary")
    scheduleds = ScheduledCommand.objects.filter(active=True)

    for s in scheduleds:
        check_if_should_run(s, now)


def check_if_should_run(scheduled, now):

    s = ScheduledCommand.objects.get(id=scheduled.id)
    d = scheduled.execution_date_or_start_date

    if now > d:
        if s.type == 'once' and s.last_execution_log is None:
            send_scheduled(s)

        elif s.type != 'once' and s.seconds_between_executions:
            if s.last_execution_log == None:
                send_scheduled(s)

            else:
                send_d = s.last_execution_log.send_date

                delta = (now - send_d)
                delta = delta.total_seconds()

                if s.execution_end_date_if_repeating and now >= s.execution_end_date_if_repeating:
                    return

                if delta > s.seconds_between_executions:
                    send_scheduled(s)






def send_scheduled(s, turn_off=False):
    mac = s.registered_chip.mac

    if settings.BLUETOOTH_SERVER:
        cmd = {}

        cmd['c'] = s.command.id

        if s.f != 0:
            cmd['f'] = '%s' % s.f

        if s.p != 0:
            cmd['p'] = '%s' % s.p

        if s.n != 0:
            cmd['n'] = '%s' % s.n


        logs = settings.BLUETOOTH_SERVER.send_commands_for_devices([{'mac': mac, 'commands':[cmd]}], True)

        if len(logs) > 0:
            log = logs[0]

            if log.successful == False and s.retry_if_fails:
                log = retry_send_5_times(mac, log, [cmd])

            s.last_execution_log = log

            if log.successful == True and s.send_turn_off_command_in_seconds and s.send_turn_off_command_in_seconds > 0 and turn_off is False:
                t = ThreadTimer(s.send_turn_off_command_in_seconds, send_scheduled, kwargs={'s':s, 'turn_off':True})
                t.start()

        s.save()


def retry_send_5_times(mac, initial_log, commands):

    log =  initial_log
    for i in range(0, 5):
        if settings.BLUETOOTH_SERVER:
            logs = settings.BLUETOOTH_SERVER.send_commands_for_devices([{'mac': mac, 'commands':commands}], True)

            if len(logs) > 0:
                log = logs[0]

                if log.successful == True:
                    break

    return log


