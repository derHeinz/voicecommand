class VoiceCommand():

    def can_process(self, vc):
        return False

    def process(self, vc):
        pass


class ConfigurableVoiceCommand(VoiceCommand):

    def __init__(self, config=None):
        self._load_config(config)
