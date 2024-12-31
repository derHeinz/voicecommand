from .voicecommand import ConfigurableVoiceCommand
from .process_result import ProcessResult


class SwitchItemsVoiceCommand(ConfigurableVoiceCommand):

    COMMAND_MAPPINGS = {"an": "ON", "anmachen": "ON", "ein": "ON", "einschalten": "ON",
                        "aus": "OFF", "ausschalten": "OFF", "ausmachen": "OFF"
                        }

    def _load_config(self, data):
        self.WORDS_TO_ITEMS = data

    def _openhab_items(self, vc):
        res = []
        for keyword in self.WORDS_TO_ITEMS:
            if keyword.lower() in vc.lower():
                res.append(self.WORDS_TO_ITEMS[keyword])
        return res

    def _signal_word(self, vc):
        for k in self.COMMAND_MAPPINGS.keys():
            if k in vc.lower():
                return k
        return None

    def _contains_signal_word(self, vc):
        sw = self._signal_word(vc)
        if sw is None:
            return False
        return True

    def can_process(self, vc):
        return self._contains_signal_word(vc)

    def process(self, vc) -> ProcessResult:
        signalword = self._signal_word(vc)
        command = self.COMMAND_MAPPINGS[signalword]
        extracted_items = self._openhab_items(vc)

        from raspberrypi_python import postopenhab
        for item in extracted_items:
            postopenhab.post_value_to_openhab(item, command)

        items_text = ', '.join(extracted_items)

        return ProcessResult("Ein/Aus Schalter", True, "Setzte " + items_text + " auf " + command)
