#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

def load_config_file(filename):
    config_filename = os.path.dirname(__file__) + filename
    with open(config_filename) as data_file:    
        data = json.load(data_file)
        return data