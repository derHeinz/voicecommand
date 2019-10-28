#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from .alarmclockvoicecommand import AlarmClockVoiceCommand

class TestAlarmClockVoiceCommand(unittest.TestCase):
    
    def _testee(sef):
        return AlarmClockVoiceCommand({"ip": "1.1.1.1"})
        
    def test_can_process(self):
        positive_list = ["Wecker auf 8", "Wecker auf acht", "Stelle Wecker auf 6 Uhr 30", 
        "Stelle Wecker auf 6 Uhr dreißg", "Stelle Wecker auf sechs Uhr dreißig"]
        
        for text in positive_list:
            self.assertTrue(self._testee().can_process(text))
            
        negative_list = ["weck mich um 6", "Wecker um sieben Uhr", "Wecken um zehn"]
        for text in negative_list:
            self.assertFalse(self._testee().can_process(text))
            
    def test_extract_time(self):
        self.assertEqual("8:00", self._testee()._extract_time("Wecker auf 8 Uhr"))
        self.assertEqual("8:00", self._testee()._extract_time("Wecker auf 8"))
        self.assertEqual("10:20", self._testee()._extract_time("Stelle Wecker auf 10 Uhr 20"))
        
        self.assertEqual("11:30", self._testee()._extract_time("Stelle Wecker auf 11 30"))
        self.assertEqual("11:30", self._testee()._extract_time("Stelle Wecker auf 11 30 Uhr"))
        
        self.assertEqual("11:30", self._testee()._extract_time("Wecker auf elf dreißig"))
        self.assertEqual("11:30", self._testee()._extract_time("Stelle Wecker auf elf dreißig"))
        self.assertEqual("11:30", self._testee()._extract_time("Stelle Wecker auf elf dreißig Uhr"))