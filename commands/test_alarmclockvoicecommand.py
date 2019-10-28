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
    
    def _legal_time_