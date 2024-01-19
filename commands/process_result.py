#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ProcessResult():

    def __init__(self, t, s, m):
        self.type = t
        self.success = s
        self.message = m

    def is_sucess(self):
        return self.success

    def is_error(self):
        return not self.success

    def get_type(self):
        return self.type

    def get_message(self):
        return self.message
