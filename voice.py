import sys
import json
import inspect
import os

from commands.process_result import ProcessResult
from commands.playvoicecommand import PlayVoiceCommand
from commands.switchitemsvoicecommand import SwitchItemsVoiceCommand
from commands.alarmclockvoicecommand import AlarmClockVoiceCommand
from commands.playyoutubecommand import PlayYoutubeVoiceCommand

import config_helper

def load_processors():
    processors = []
    processors.append(load_processor("/words_to_items.json", SwitchItemsVoiceCommand))
    processors.append(load_processor("/dlna.json", PlayVoiceCommand))
    processors.append(load_processor("/alarmclock.json", AlarmClockVoiceCommand))
    processors.append(load_processor("/playyoutube.json", PlayYoutubeVoiceCommand))
    return processors
    
def load_processor(config_filename, clazz):
    data = config_helper.load_config_file(config_filename)
    return clazz(data)
    
def reference_modules():
    cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))    
    cmd_parent_folder = os.path.normpath(os.path.join(cmd_folder, ".."))
    sys.path.insert(0, cmd_parent_folder)
    
def send_data_to_openhab(result, vc):
    config_data = config_helper.load_config_file("/voiceconfig.json")
    
    msg = "nicht verarbeitbar: '{}'".format(vc)
    processor = "kein Prozessor"
    if result is not None:
        msg = result.get_message()
        processor = result.get_type()
    
    from raspberrypi_python import postopenhab
    postopenhab.post_value_to_openhab(config_data['openhab_processor_name_item'], processor)
    postopenhab.post_value_to_openhab(config_data['openhab_processor_result_item'], msg)
    
    
    
def log(txt):
    print(txt)
    
if (len(sys.argv) > 1):
    vc = sys.argv[1]
    log(vc)
    procs = filter(lambda p : p.can_process(vc), load_processors())
    
    reference_modules()
    result = None
    
    for p in procs:
        log("processing {}".format(p))
        result = p.process(vc)

    send_data_to_openhab(result, vc)
