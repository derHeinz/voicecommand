import sys
import json
import inspect
import os

from commands.playvoicecommand import PlayVoiceCommand
from commands.switchitemsvoicecommand import SwitchItemsVoiceCommand
from commands.alarmclockvoicecommand import AlarmClockVoiceCommand
import config_helper

def load_processors():
    processors = []
    processors.append(load_processor("/words_to_items.json", SwitchItemsVoiceCommand))
    processors.append(load_processor("/dlna.json", PlayVoiceCommand))
    processors.append(load_processor("/alarmclock.json", AlarmClockVoiceCommand))
    return processors
    
def load_processor(config_filename, clazz):
    data = config_helper.load_config_file(config_filename)
    return clazz(data)
    
def reference_modules():
    cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))    
    cmd_parent_folder = os.path.normpath(os.path.join(cmd_folder, ".."))
    sys.path.insert(0, cmd_parent_folder)

def log(txt):
    print(txt)
    #f = open("/tmp/a.txt","a+")
    #f.write(txt + "\n")
    #f.close()
    
if (len(sys.argv) > 1):
    vc = sys.argv[1]
    log(vc)
    procs = filter(lambda p : p.can_process(vc), load_processors())
    
    reference_modules()
    
    for p in procs:
        log("processing {}".format(p))
        p.process(vc)
