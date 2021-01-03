#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
    
def _merge(data, data_to_merge, path=None):
    "merges data_to_merge into data"
    # see https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries/7205107#7205107
    if path is None: path = []
    for key in data_to_merge:
        if key in data:
            if isinstance(data[key], dict) and isinstance(data_to_merge[key], dict):
                _merge(data[key], data_to_merge[key], path + [str(key)])
            elif data[key] == data_to_merge[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            data[key] = data_to_merge[key]
    return data

def load_config_files(*filenames):
    res = {}
    for filename in filenames:
        config_filename = os.path.dirname(__file__) + filename
        with open(config_filename) as data_file:    
            data = json.load(data_file)
            res = _merge(res, data)
    return res