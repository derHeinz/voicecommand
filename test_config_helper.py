import unittest
import copy
import json
import os

import config_helper

cfg_1 = {'a': {'A': 1, 'B': 2}, 'b': {'B': 3}} # default
cfg_2 = {'a': {'C': 90}}  # mergeable with cfg_1
cfg_3 = {'b': {'B': 42}}  # mergeable with cfg_2, confliciting with cfg_2 at b.B


class Testconfig_helper(unittest.TestCase):

    def _merge_with_deepcopy(self, data_one, data_two):
        return config_helper._merge(copy.deepcopy(data_one), copy.deepcopy(data_two))

    def _check_contains_cfg_1_elements(self, res):
        self.assertEqual(1, res['a']['A'])
        self.assertEqual(2, res['a']['B'])
        self.assertEqual(3, res['b']['B'])

    def _check_contains_cfg_2_elements(self, res):    
        self.assertEqual(90, res['a']['C'])

    def _check_contains_cfg_3_elements(self, res):    
        self.assertEqual(42, res['b']['B'])

    def test_merge(self):

        res = self._merge_with_deepcopy(cfg_1, cfg_2) # should work
        self._check_contains_cfg_1_elements(res)
        self._check_contains_cfg_2_elements(res)

        res = self._merge_with_deepcopy(cfg_2, cfg_1) # should work vice-versa
        self._check_contains_cfg_1_elements(res)
        self._check_contains_cfg_2_elements(res)

        res = self._merge_with_deepcopy(cfg_2, cfg_3)
        self._check_contains_cfg_2_elements(res)
        self._check_contains_cfg_3_elements(res)

        self._merge_with_deepcopy(cfg_3, cfg_2)
        self._check_contains_cfg_2_elements(res)
        self._check_contains_cfg_3_elements(res)

        # assume error
        with self.assertRaises(Exception):
            self._merge_with_deepcopy(cfg_1, cfg_3)
        with self.assertRaises(Exception):
            self._merge_with_deepcopy(cfg_3, cfg_1)

    def setUp(self):

        # assert cfgs are unchanged.
        self._check_contains_cfg_1_elements(cfg_1)
        self._check_contains_cfg_2_elements(cfg_2)
        self._check_contains_cfg_3_elements(cfg_3)

        # output into files
        with open('cfg_1.json', 'w') as outfile:
            json.dump(cfg_1, outfile)
        with open('cfg_2.json', 'w') as outfile:
            json.dump(cfg_2, outfile)
        with open('cfg_3.json', 'w') as outfile:
            json.dump(cfg_3, outfile)

    def tearDown(self):
        os.remove('cfg_1.json')
        os.remove('cfg_2.json')
        os.remove('cfg_3.json')

    def test_load(self):
        res = config_helper.load_config_files("/cfg_1.json", "/cfg_2.json")
        self._check_contains_cfg_1_elements(res)
        self._check_contains_cfg_2_elements(res)

        res = config_helper.load_config_files("/cfg_2.json", "/cfg_1.json")
        self._check_contains_cfg_1_elements(res)
        self._check_contains_cfg_2_elements(res)

        res = config_helper.load_config_files("/cfg_2.json", "/cfg_3.json")
        self._check_contains_cfg_2_elements(res)
        self._check_contains_cfg_3_elements(res)

        res = config_helper.load_config_files("/cfg_3.json", "/cfg_2.json")
        self._check_contains_cfg_2_elements(res)
        self._check_contains_cfg_3_elements(res)

        with self.assertRaises(Exception):
            config_helper.load_config_files("/cfg_1.json", "/cfg_3.json")
        with self.assertRaises(Exception):
            config_helper.load_config_files("/cfg_3.json", "/cfg_1.json")
