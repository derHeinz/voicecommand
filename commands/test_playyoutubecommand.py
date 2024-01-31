import unittest
from .playyoutubecommand import PlayYoutubeVoiceCommand


class TestPlayYoutubeVoiceCommand(unittest.TestCase):

    def _testee(sef):
        return PlayYoutubeVoiceCommand({"media_controller_url": "url", "youtube_audio_provider_url": "url"})

    def test_can_process(self):
        positive_list = ["Youtube spiele Queen", "youtube spiel Heavy von Queen", "youtube spiel Another One bite the dust", 
                         "YouTube spiele meine Oma fährt im Hühnerstall Motorrad"]
        for text in positive_list:
            self.assertTrue(self._testee().can_process(text))

        negative_list = ["youtube Queen", "Queen youtube spiel"]
        for text in negative_list:
            self.assertFalse(self._testee().can_process(text))

    def test_extract_search_query(self):
        self.assertEqual("Show must go on", self._testee()._extract_search_query("Youtube spiele Show must go on"))
        self.assertEqual("Show must go on", self._testee()._extract_search_query("YouTube spiel Show must go on"))
        self.assertEqual("Show must go on", self._testee()._extract_search_query("Youtube spiel Show must go on;"))
        self.assertEqual("Queen", self._testee()._extract_search_query("Youtube spiele Queen"))
