#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

class VoiceCommand():
    
    def can_process(self, vc):
        return False
        
    def process(self, vc):
        pass
        
class ConfigurableVoiceCommand(VoiceCommand):

    def __init__(self, config=None):
        self._load_config(config)
            
    def _config_filename(self):
        pass
