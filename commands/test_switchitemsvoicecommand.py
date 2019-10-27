import unittest
from .switchitemsvoicecommand import SwitchItemsVoiceCommand

class TestSwitchItemsVoiceCommand(unittest.TestCase):

    def _testee(sef):
        return SwitchItemsVoiceCommand({"Radio": "RadioPowerOpenhabItem", "Fernseher": "TVPower"})
        
    def test_can_process(self):
        self.assertTrue(self._testee().can_process("Radio anschalten"))
        self.assertTrue(self._testee().can_process("Radio ein"))
        self.assertTrue(self._testee().can_process("Radio anmachen"))
        self.assertTrue(self._testee().can_process("Radio einschalten"))
        
        self.assertTrue(self._testee().can_process("Radio aus"))
        self.assertTrue(self._testee().can_process("Radio ausmachen"))
        self.assertTrue(self._testee().can_process("Radio ausschalten"))
        
    def test_openhab_items(self):
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ein"))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("ausschalten Radio"))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ausmachen"))
        self.assertIn("TVPower", self._testee()._openhab_items("Bitte Fernseher ausmachen"))
        
