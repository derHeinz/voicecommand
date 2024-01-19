import unittest
from .switchitemsvoicecommand import SwitchItemsVoiceCommand


class TestSwitchItemsVoiceCommand(unittest.TestCase):

    def _testee(sef):
        return SwitchItemsVoiceCommand({"Radio": "RadioPowerOpenhabItem", "Fernseher": "TVPower"})

    def test_can_process(self):
        positive_list = ["Radio anschalten", "Radio ein", "Radio anmachen", "Radio einschalten",
                         "Radio aus", "Radio ausmachen", "Radio ausschalten", "Radio ausschalten.", "Radio anmachen."]

        for text in positive_list:
            self.assertTrue(self._testee().can_process(text))

    def test_openhab_items(self):
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ein"))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ein."))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ein "))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("ausschalten Radio"))
        self.assertIn("RadioPowerOpenhabItem", self._testee()._openhab_items("Radio ausmachen"))
        self.assertIn("TVPower", self._testee()._openhab_items("Bitte Fernseher ausmachen"))
        self.assertIn("TVPower", self._testee()._openhab_items("Bitte Fernseher ausmachen."))
        self.assertIn("TVPower", self._testee()._openhab_items("Bitte Fernseher ausmachen "))
