


var get_selected_chips = function () {
    var chip_ids = [];
    $.each($("input[name='chip_checkbox']:checked"), function(){
        chip_ids.push(parseInt($(this).val()));
    });

    return chip_ids;
};

var get_selected_commands = function () {
    var commands = [];
    $.each($("input[name='command_checkbox']:checked"), function(){
        console.log("cmd checkbox");
        console.log($(this));
        commands.push($(this).val());
    });

    return commands;
};

var get_checkbox_values = function(){
    var chip_ids = get_selected_chips();


    var commands = get_selected_commands();

    console.log("chip ids");
    console.log(chip_ids);
    console.log("commands");
    console.log(commands);

    var commands_by_chip = {};

    for (var i = 0; i < chip_ids.length; i++) {
        var chip_id = chip_ids[i];
        console.log(chip_id);

        var chip_id_str = chip_id.toString();
        var chip_cmds = [];

        for (var a = 0; a < commands.length; a++) {
            console.log('cmd');

            var cmd = commands[a];
            console.log(cmd);

            if (cmd.startsWith(chip_id_str)) {
                var re = new RegExp(chip_id_str + '#', "g");

                var order_number_id = "command_order_" + cmd;
                var order = document.getElementById(order_number_id).value;


                var frequency_id = "frequency_" + cmd;
                var frequency = '';
                if (document.getElementById(frequency_id)) {
                    frequency = document.getElementById(frequency_id).value;
                }


                var pulse_id= "pulse_" + cmd;
                var pulse = '';
                if (document.getElementById(pulse_id)) {
                    pulse = document.getElementById(pulse_id).value;
                }

                var number_id= "number_" + cmd;
                var number = '';
                if (document.getElementById(number_id)) {
                    number = document.getElementById(number_id).value;
                }


                chip_cmds.push({
                    'c': cmd.replace(re, ''),
                    'o': order,
                    'f':frequency,
                    'p': pulse,
                    'n': number
                });

                console.log("push");
                console.log(chip_cmds);

            }
        }

        if (chip_cmds.length > 0) {


            commands_by_chip[chip_id] = chip_cmds;
        }
    }
    console.log(commands_by_chip);
    return encodeURIComponent(JSON.stringify(commands_by_chip))
};


var apply_to_all_selected = function(source_id) {
    var commands = get_selected_commands();

    var source_cmds = {};

    for (var a = 0; a < commands.length; a++) {
        console.log('cmd');

        var cmd = commands[a];
        console.log(cmd);

        if (cmd.startsWith(source_id)) {
            var re = new RegExp(source_id + '#', "g");

            var order_number_id = "command_order_" + cmd;
            var order = document.getElementById(order_number_id).value;


            var frequency_id = "frequency_" + cmd;
            var frequency = '';
            if (document.getElementById(frequency_id)) {
                frequency = document.getElementById(frequency_id).value;
            }

            var pulse_id = "pulse_" + cmd;
            var pulse = '';
            if (document.getElementById(pulse_id)) {
                pulse = document.getElementById(pulse_id).value;
            }

            var number_id = "number_" + cmd;
            var number = '';
            if (document.getElementById(number_id)) {
                number = document.getElementById(number_id).value;
            }

            source_cmds[cmd.replace(re, '')] = {
                'c': cmd.replace(re, ''),
                'o': order,
                'f': frequency,
                'p': pulse,
                'n': number
            };
        }
    }

    var chips = get_selected_chips();

    $.each($("input[name='command_checkbox']"), function(){
        console.log("cmd checkbox");
        for (i = 0; i < chips.length; i++) {
            var ch = chips[i];

            for (var key in source_cmds) {
                if (source_cmds.hasOwnProperty(key)) {
                    if($(this).val().startsWith(ch) && $(this).val().endsWith('#' + key)) {
                        $(this).prop("checked", true);


                        var cmd_d = source_cmds[key];

                        if (cmd_d['o'] != '') {
                            var order_number_id = "command_order_" + ch + '#' + key;
                            console.log(order_number_id);
                            document.getElementById(order_number_id).value = cmd_d['o']

                        }


                        if (cmd_d['f'] != '') {
                            var item_id = "frequency_" + ch + '#' + key;
                            var el = document.getElementById(item_id);
                            if (el) {
                                el.value = cmd_d['f'];
                            }
                        }

                        if (cmd_d['p'] != '') {
                            var item_id = "pulse_" + ch + '#' + key;
                            var el = document.getElementById(item_id);
                            if (el) {
                                el.value = cmd_d['p'];
                            }
                        }

                        if (cmd_d['n'] != '') {
                            var item_id = "number_" + ch + '#' + key;
                            var el = document.getElementById(item_id);
                            if (el) {
                                el.value = cmd_d['n'];
                            }
                        }


                    }
                }
            }

        }
    });

};

var select_all = function() {
    var on_or_off = true;

    $.each($("input[name='select_all']"), function() {
        on_or_off = $(this).prop("checked");

    });

    $.each($("input[name='chip_checkbox']"), function(){
        $(this).prop("checked", on_or_off);
    });
};

var stopEventPropagation = function(e) {

    event.stopPropagation();
};

var save_text = function() {
    var txt = document.getElementById('shared_text').value;
     $.post("mouse_viewer_save_text",
        JSON.stringify({text: txt}),
        function(data, status){});
};

window.doTimezoneStuff = function(tzone, tdelta) {
    var lcl_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    var date = new Date();
    var lcl_offset = date.getTimezoneOffset() / 60;

    console.log(lcl_offset);
    console.log(tdelta)
    var delta = lcl_offset + parseInt(tdelta);

    var dif = "";
    if (delta < 0) {
        dif = "" + Math.abs(delta) + " hours ahead";
    }
    else if (delta == 0) {
        dif = "at the same time";
    }
    else {
        dif = "" + Math.abs(delta) + " hours behind";
    }
    var s = "Server Timezone: " + tzone + " ----- Your Timezone: " + lcl_timezone + " ----- You are " + dif;

    document.getElementById('timezone_p').innerText = s;
};

var open_csv = function (url) {

  var win = window.open(url, '_blank');

    if (win) {
        //Browser has allowed it to be opened
        win.focus();
    } else {
        //Browser has blocked it
        alert('Please allow popups for this website');
    }
};