#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from .process_result import ProcessResult

class TestProcessResult(unittest.TestCase):

    def test_process_result(self):
        p = ProcessResult("test", True, "Some message")
        self.assertTrue(p.is_sucess())
        self.assertFalse(p.is_error())
        self.assertEqual("Some message", p.get_message())
        self.assertEqual("test", p.get_type())
        
        p = ProcessResult("test", False, "Error 1")
        self.assertFalse(p.is_sucess())
        self.assertTrue(p.is_error())
        self.assertEqual("Error 1", p.get_message())