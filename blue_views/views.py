from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from itertools import groupby
from django.forms.models import model_to_dict
from django.db import transaction
import copy
import json
from io import StringIO
import csv
from functools import wraps
import time
from BoulderBlueServerWebApp.BoulderBlueServerWebApp import settings
from BoulderBlueServerWebApp.blue_views.models import *
#import matplotlib.pyplot as plt
import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import FixedTicker
import math
from dateutil.tz import tzlocal
import time
from bokeh.resources import CDN
from bokeh.embed import file_html
localtimezone = time.tzname


def localTzOffset(): #time zone offset
    if time.daylight:
        offsetHour = time.altzone / 3600
    else:
        offsetHour = time.timezone / 3600

    return offsetHour


def render_to(template=None):
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            markup = render(request, tmpl, output)
            return markup

        return wrapper

    return renderer

@login_required
@staff_member_required
@never_cache
@render_to('index.html')
def index(request):
    with transaction.atomic():
        registered = RegisteredChip.objects.all()
        discovered = DiscoveredChip.objects.all()

        def process_chip_data(chips):
            chip_data = []

            for chip in chips:
                chip_data.append(
                    {'mac': chip.mac, 'name': chip.name, 'lastSeen': str(chip.last_seen), 'visible': chip.visible})

            return chip_data

        chip_groups = []

        connected = []

        regs = process_chip_data(registered)

        conn_devices = settings.BLUETOOTH_SERVER.connected_devices
        print("conn_devices %s" % conn_devices)

        # very bad code, but I don't want to the structures of the dicts
        for c in regs:
            print("reg ::::: %s", c)

            for serial_port in conn_devices.keys():
                conns = conn_devices[serial_port]

                for con in conns:
                    mac = con['mac']
                    print("       con %s", con)
                    if mac == c['mac']:
                        if 'exception' in con and con['exception'] != '':
                            c['exception'] = "Conn Error %s" % con['exception']
                            print("continue because of crap")
                            continue

                        print("appending")
                        connected.append(c)
                        break

        con = {'id': 'connected', 'name': 'Connected Chips', 'chips': connected, 'count': len(connected)}

        reg = {'id': 'registered', 'name': 'Registered Chips', 'chips': regs, 'count': len(registered)}

        disc = {'id': 'discovered', 'name': 'Discovered Chips', 'chips': process_chip_data(discovered),
                'count': len(discovered)}

        chip_groups.append(con)
        chip_groups.append(reg)
        chip_groups.append(disc)

        textB = list(TextBox.objects.all())
        text = ""
        if len(textB) >= 1:
            text = textB[0].text

        return {'chipGroups': chip_groups, 'tzone': localtimezone[0], 'tdelta': localTzOffset(), 'text': text}


@staff_member_required
@never_cache
@transaction.atomic
def register(request, mac=None):
    dis = DiscoveredChip.objects.get(mac=mac)

    reg = RegisteredChip()
    reg.mac = dis.mac
    reg.name = dis.name
    reg.last_seen = dis.last_seen
    reg.visible = True

    reg.save()
    dis.delete()
    settings.BLUETOOTH_SERVER.request_client_to_register_to_new_device(mac)

    return redirect('mouse_viewer')


@staff_member_required
@never_cache
@transaction.atomic
def unregister(request, mac=None):
    print(request.method)
    dis = RegisteredChip.objects.get(mac=mac)
    dis.delete()

    return redirect('mouse_viewer')


@staff_member_required
@never_cache
@render_to('select_commands.html')
def select_commands(request):
    conn_devs = []

    if settings.BLUETOOTH_SERVER:
        conn_devs = settings.BLUETOOTH_SERVER.get_connected_macs()

    chips = list(RegisteredChip.objects.filter(mac__in=conn_devs))

    print("conn devs %s" % conn_devs)
    print(" chips %s" % len(chips))
    chip_data = []

    conn_devices = settings.BLUETOOTH_SERVER.connected_devices
    print("conn_devices %s" % conn_devices)

    useful_chips = []
    # very bad code, but I don't want to the structures of the dicts
    for c in chips:
        for serial_port in conn_devices.keys():
            conns = conn_devices[serial_port]

            for con in conns:
                mac = con['mac']

                if mac == c.mac:
                    if 'exception' in con and con['exception'] != '':
                        continue

                    useful_chips.append(c)
                    break

    for chip in useful_chips:
        chip_dic = {'mac': chip.mac, 'name': chip.name, 'id': chip.id}
        if chip.connection_exception:
            chip_dic['exception'] = chip.connection_exception
        chip_data.append(chip_dic)

    chips = sorted(chip_data, key=lambda k: k["name"])

    commands = ChipCommand.objects.all().order_by('category__index').prefetch_related('category')

    commands_as_dict = []
    for command in commands:
        c = model_to_dict(command)
        c['category_index'] = command.category.index
        c['category_name'] = command.category.name

        commands_as_dict.append(c)

    commands = sorted(commands_as_dict, key=lambda k: (k["category_name"], k["command"]))

    for chip in chips:
        chip['commands'] = []

        for command in commands:
            c = copy.deepcopy(command)
            c['command_id'] = str(chip['id']) + '#' + command['command']
            chip['commands'].append(c)

    dic = {'tzone': localtimezone[0], 'tdelta': localTzOffset()}
    dic['chips_and_commands'] = chips
    dic['asdf'] = 'asdf'  # just needed for some trickery
    import pprint
    pprint.pprint(dic)

    textB = list(TextBox.objects.all())
    text = ""
    if len(textB) >= 1:
        text = textB[0].text

    dic['text'] = text
    return dic


@staff_member_required
@never_cache
@render_to('sent_selected_commands.html')
def send_selected_commands(request, chip_commands=None):
    print("send selected commands %s" % chip_commands)
    # 입력받은 명령이 없을 경우(선택 없을 경우) 에러메시지 출력
    if chip_commands is None or chip_commands == '{}':
        dic = {}
        dic['big_error'] = "No commands selected!"
        return dic
    #명령 있을 경우 받아들이기
    chip_commands = json.loads(chip_commands)
    print("send selected commands 2 %s" % chip_commands)
    #명령 입력받을 공간 생성
    device_cmds = []
    #명령어 스트링에 있는 문자 하나하나를 받아오는 함수
    for c_id in chip_commands:
        cs = chip_commands[c_id]
        cs = sorted(cs, key=lambda k: (k["o"]))

        mac = RegisteredChip.objects.get(id=int(c_id)).mac

        command_cs = []

        for c in cs:
            # {'c':command, 'o': order}
            command_cs.append(c['c'])

        cmds = list(ChipCommand.objects.filter(command__in=command_cs))
        cmds_to_send = []

        for c in cs:
            for cc in cmds:
                if c['c'] == cc.command:
                    c['c'] = cc.id
                    cmds_to_send.append(c)
                    break

        print("cmds to send %s" % cmds_to_send);

        if len(cmds_to_send) > 0:
            device_cmds.append({'mac': mac, 'commands': cmds_to_send})

    print("device commands %s" % device_cmds)
    # logs same with bt_handler.py
    if settings.BLUETOOTH_SERVER:
        logs = settings.BLUETOOTH_SERVER.send_commands_for_devices(device_cmds)

    else:
        dic = {}
        dic['big_error'] = "No BT interface found!"

        return dic

    temp_logs = []
    for log in logs:
        logx = model_to_dict(log)
        logx['send_date'] = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        logx['command_name'] = log.command.name
        logx['command_command'] = log.command.command
        logx['command_category'] = log.command.category.name
        logx['chip_name'] = log.registered_chip.name


        if log.t_result != None:
            print("t_result isn't None")
            logx['t_result'] = log.t_result
            logx['type_data'] = log.type_data
            recvData = ReceivedData()
            recvData.received_time = log.send_date
            recvData.send_chip = log.registered_chip
            recvData.t_result = log.t_result
            recvData.type_data = log.type_data

            recvData.save()


        if log.f:
            logx['f'] = log.f

        if log.p:
            logx['p'] = log.p

        if log.n:
            logx['n'] = log.n

        temp_logs.append(logx)

    dic = {'tzone': localtimezone[0], 'tdelta': localTzOffset()}
    dic['logs'] = sorted(temp_logs, key=lambda k: k["send_index"])

    textB = list(TextBox.objects.all())
    text = ""
    if len(textB) >= 1:
        text = textB[0].text

    dic['text'] = text
    return dic


@staff_member_required
@never_cache
@render_to('log.html')
def log(request):
    logs = CommandLog.objects.all().order_by('-send_date')
    temp_logs = []

    failed_command_string = ""
    for log in logs:
        logx = model_to_dict(log)
        logx['send_date'] = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        logx['command_name'] = log.command.name
        logx['command_command'] = log.command.command
        logx['command_category'] = log.command.category.name
        logx['chip_name'] = log.registered_chip.name
        logx['chip_mac'] = log.registered_chip.mac
        logx['scheduled'] = log.scheduled
        logx['t_result'] = log.t_result
        logx['type_data'] = log.type_data

        #recvData.send_chip = log.registered_chip.name
        #recvData.received_time = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        #recvData.t_result = log.t_result

        if log.f:
            logx['f'] = log.f

        if log.p:
            logx['p'] = log.p

        if log.n:
            logx['n'] = log.n

        temp_logs.append(logx)

    textB = list(TextBox.objects.all())
    text = ""
    if len(textB) >= 1:
        text = textB[0].text

    return {'logs': temp_logs, 'tzone': localtimezone[0], 'tdelta': localTzOffset(), 'text': text}


@staff_member_required
@never_cache
def run_test(request):
    reg_chips = RegisteredChip.objects.filter()

    from time import sleep

    commands = ["a", "d", "f", 'm']

    macs = []

    for chip in reg_chips:
        macs.append(chip.mac)

    send_commands_with_break(commands, macs)

    sleep(4)

    commands = ["r"]
    macs = []

    for chip in reg_chips:
        macs.append(chip.mac)

    send_commands_with_break(commands, macs)
    sleep(10)

    commands = ["s"]
    macs = []
    for chip in reg_chips:
        macs.append(chip.mac)

    send_commands_with_break(commands, macs)

    sleep(3)
    commands = ["r"]
    error_count = 0

    macs = []
    for chip in reg_chips:
        macs.append(chip.mac)

    err_c = send_commands_with_break(commands, macs)

    error_count = error_count + err_c

    return HttpResponse("Test completed! Error count: %s" % error_count, 200)


def send_commands_with_break(commands, macs):
    commands_to_send = []
    for com in commands:
        commands_to_send.append(com)

    cmds = list(ChipCommand.objects.filter(command__in=commands_to_send))

    commands = []
    for c in commands_to_send:
        for cc in cmds:
            if c == cc.command:
                commands.append(cc.id)
                break

    send = []

    for mac in macs:
        send.append({'mac': mac, 'commands': commands})

    if settings.BLUETOOTH_SERVER:
        logs = settings.BLUETOOTH_SERVER.send_commands_for_devices(send)
        errs = 0
        for log in logs:
            if log.successful == False:
                errs += 1
        return errs
    return 0


@staff_member_required
@never_cache
def csv_out(request):
    logs = CommandLog.objects.all().order_by('-send_date')

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        ["date", "command name", "command category", "chip name", "command", "f", "p", "n", "scheduled", "result", "t result"])

    for log in logs:
        date = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        name = log.command.name
        command = log.command.command
        category = log.command.category.name
        chip_name = log.registered_chip.name
        scheduled = log.scheduled

        f = ''
        if log.f:
            f = log.f

        p = ''
        if log.p:
            p = log.p

        n = ''
        if log.n:
            n = log.n

        result = 'success'
        if log.error and log.error != '':
            result = 'Error %s' % log.error

        t_result = log.t_result

        writer.writerow(
            [date, name, category, chip_name, command, f, p, n, scheduled, result, t_result])

    final_csv = output.getvalue()

    output.close()

    return HttpResponse(final_csv, 200)


from django.views.decorators.csrf import csrf_exempt
@staff_member_required
@never_cache
@render_to('received_data_log.html')
def received_data_log(request):
    logs = ReceivedData.objects.all().order_by('-received_time')
    temp_logs = []
    failed_command_string = ""
    for log in logs:
        logx = model_to_dict(log)
        logx['received_time'] = log.received_time.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        logx['send_chip'] = log.send_chip.name
        logx['t_result'] = log.t_result
        logx['type_data'] = log.type_data

# 지금은 success만 출력되는 상태임. 문제 해결방안을 찾아야함.
        #recvData = ReceivedData()
        #recvData.send_chip = log.registered_chip.name
        #recvData.received_time = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        #recvData.t_result = log.command.t_result

        temp_logs.append(logx)

    textB = list(TextBox.objects.all())
    text = ""
    if len(textB) >= 1:
        text = textB[0].text

    return {'logs': temp_logs, 'tzone': localtimezone[0], 'tdelta': localTzOffset(), 'text': text}


@staff_member_required
@never_cache
def received_data_csv_out(request):
    logs = CommandLog.objects.all().order_by('-send_date')

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        ["date", "command name", "command", "chip name", "t_result"])

    for log in logs:
        date = log.send_date.strftime("%Z%z %Y-%m-%d %H:%M:%S.%f")[:-3]
        name = log.command.name
        command = log.command.command
        chip_name = log.registered_chip.name
        t_result = log.t_result

        writer.writerow(
            [date, name, command, chip_name, command, t_result])

    final_csv = output.getvalue()

    output.close()

    return HttpResponse(final_csv, 200)

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@never_cache
def save_text(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    textB = list(TextBox.objects.all())
    if len(textB) >= 1:
        textB[0].text = body['text']
        textB[0].save()
    else:
        textB = TextBox()
        textB.text = body['text']
        textB.save()

    return HttpResponse("", 200)
    
 
@staff_member_required
@never_cache
@render_to('home.html')
def home(request):
	logs = CommandLog.objects.all().order_by('-send_date')
	chip_data = [
            {
                "name":'Mouse9',
                "connection_status":'Success',
                "recent_log": {
                    "command": 'A',
                    "status": 'Success'
                },
                "scheduled_commands":'None'
            }
        ]

	"""
	FAKE_DATA CHART
	"""
	T = [22.5, 22.9, 25.6, 25.0, 20.3]
	P = [760, 730, 769, 768, 700]
	H = [30, 40, 25, 43, 60]
	timestamp = ['May 1st','May 2nd', 'May 3rd','May 5th', 'May 10th']
	# output to static HTML file
	#output_file("log_lines.html")
	x = [i for i in range(len(timestamp))]
	# create a new plot
	curdoc().theme ='light_minimal'
	p = figure(
   	tools="pan,box_zoom,reset,save",
   	title="Lab environment",
   	x_axis_label='Date', y_axis_label='Params'
	)

	# add some renderers
	p.line(x, T, legend="Temperature",line_color='blue')
	p.circle(x, T, legend="Temperature", fill_color="white", size=8)
	p.line(x, P, legend="Pressure", line_width=3, line_color='gray')
	p.line(x, H, legend="Humidity", line_color="aqua")
	label_overrides = {}
	for i in x:
	    label_overrides[i]=timestamp[i]
	p.xaxis.ticker = x
	p.xaxis.major_label_overrides = label_overrides
	p.xaxis.major_label_orientation = math.pi/4
	html = file_html(p, CDN, "Lab Environment")
	return render(request, 'home.html', {'logs': logs, 'chip_data': chip_data, "plot":html})
def command_create(request):
	return render(request,'command_create.html',{})
	
def scheduled_commands(request):
	return render(request, 'scheduled_commands.html',{})
	
