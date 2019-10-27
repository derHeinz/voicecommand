#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .voicecommand import VoiceCommand

class AlarmClockVoiceCommand(VoiceCommand):

    START_TOKEN = ["Stelle Wecker auf", "Wecker auf", "Stelle Wecker um"]
    OFF_TOKEN = ["Wecker aus"]
    
    def __init__(self, config=None):
        self.START_TOKEN.sort(key=len, reverse=True)
        if (config == None):
            self._load_config_file()
        else:
            self._load_config(config)
        
    def _load_config_file(self):
        config_filename = os.path.dirname(__file__) + "/alarmclock.json" 
        with open(config_filename) as data_file:    
            data = json.load(data_file)
            self._load_config(data)
            
    def _load_config(self, data):
        self.ALARMCLOCKIP = data['ip']
    
    def can_process(self, vc):
        for keyword in self.START_TOKEN:
            if vc.lower().startswith(keyword.lower()):
                return True
        for keyword in self.OFF_TOKEN:
            if (vc.lower() == keyword.lower()):
                return True
        return False
        
    NUMBERS = {"eins": "1", "zwei": "2", "drei": "3", "vier": "4", "fünf": "5", 
    "sechs": "6", "sieben": "7", "acht": "8", "neun": "9", "zehn": "10", "elf": "11",
    "zwölf": "12", "dreizehn": "13", "vierzehn": "14", "fünfzehn": "15", "sechszehn": "16",
    "siebzehn": "17", "achtzehn": "18", "neunzehn": "11", "zwanzig": "20", "einundzwanzig": "21",
    "zweundzwanzig": "22", "dreiundzwanzig": "23", "dreißig": "30", "vierzig": "40", "fünfzig": "50"}

    def _number_replace(self, time):
        t = time.strip().lower()
        if (t in self.NUMBERS):
            return self.NUMBERS[t]
        return time
    
    def _legal_time_format(self, time):
        ''' method gets 'time' in one of the following formats (trailing 'Uhr' must be removed by caller).
        1. 8
        2. acht
        3. 8 20
        4. 8 Uhr 20
        5. acht Uhr 20
        6. 8 Uhr zwanzig
        7. acht Uhr zwanzig
        8. 8:20
        9. acht:20
        10. acht:zwanzig
        11. 8:zwanzig        
        '''
        time_ = time.lower().strip()
        if (":" in time_):
            # 2 parts, formats 8. to 11.
            times = time_.split(":")
            hour = self._number_replace(times[0].strip())
            minutes = self._number_replace(times[1].strip())
            return hour + ":" + minutes
            
        elif ("Uhr".lower() in time_):
            # 2 parts, formats 4. to 7.
            times = time_.split("Uhr".lower())
            hour = self._number_replace(times[0].strip())
            minutes = self._number_replace(times[1].strip())
            return hour + ":" + minutes
            
        elif (" " in time_):
            # 1 part, format 3.
            times = time_.split(" ")
            hour = self._number_replace(times[0].strip())
            minutes = self._number_replace(times[1].strip())
            return hour + ":" + minutes
            
        else:
            # format 1. to 2.
            hour = self._number_replace(time_.strip())
            return hour + ":00"
            
    def _extract_time(self, vc):
        rest = vc.lower()
        for keyword in self.START_TOKEN:
            if rest.startswith(keyword.lower()):
                rest = rest[len(keyword.lower()):]
        
        if (rest.endswith("Uhr".lower())):
            rest = rest[:-3]

        rest = rest.strip()
        time = self._legal_time_format(rest)
        return time
        
    def _is_deactivate(self, vc):
        for keyword in self.OFF_TOKEN:
            if (vc.lower() == keyword.lower()):
                return True
        return False
        
    def process(self, vc):
        
        from raspberrypi_python import radioalarmclockIntegration
        r = radioalarmclockIntegration.RadioAlarmClock(self.ALARMCLOCKIP)
        if (self._is_deactivate(vc)):
            r.set_alarm(False)
        else:
            alarmtime = self._extract_time(vc)
            r.set_alarmtime(alarmtime)
