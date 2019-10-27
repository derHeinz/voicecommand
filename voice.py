import sys
import json
import os

from commands.playvoicecommand import PlayVoiceCommand
from commands.switchitemsvoicecommand import SwitchItemsVoiceCommand
from commands.alarmclockvoicecommand import AlarmClockVoiceCommand
        
PROCESSORS = [SwitchItemsVoiceCommand(), PlayVoiceCommand(), AlarmClockVoiceCommand()]

def log(txt):
    print(txt)
    #f = open("/tmp/a.txt","a+")
    #f.write(txt + "\n")
    #f.close()
    
    
if (len(sys.argv) > 1):
    vc = sys.argv[1]
    log(vc)
    procs = filter(lambda p : p.can_process(vc), PROCESSORS)
    
    # do action
    for p in procs:
        p.process(vc)
