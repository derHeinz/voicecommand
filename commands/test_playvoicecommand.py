import unittest
from .playvoicecommand import PlayVoiceCommand


class TestPlayVoiceCommand(unittest.TestCase):

    def _testee(sef):
        return PlayVoiceCommand({"renderers": {"Radio": "url"}, "servers": {"test": "url"}})

    def test_can_process(self):
        positive_list = ["spiele Lied", "spiel Heavy von Queen", "spiel Bohemian", "spiele eine Lied", 
                         "Spiele etwas von Queen.", "spiel Show must go on.", "spiel Show must go on "]
        for text in positive_list:
            self.assertTrue(self._testee().can_process(text))

        negative_list = ["etwas ist passiert", "mache Licht an", "Fernseher aus", "Spotify spiele Titel"]
        for text in negative_list:
            self.assertFalse(self._testee().can_process(text))

    def test_parse_title_artist_target(self):
        self.assertEqual(("Show must go on", None, None), self._testee()._parse_title_artist_target("spiel Show must go on"))
        self.assertEqual(("Show must go on", None, None), self._testee()._parse_title_artist_target("spiele Show must go on"))
        self.assertEqual(("Show must go on", None, None), self._testee()._parse_title_artist_target("spiele Show must go on;"))
        self.assertEqual(("Show must go on", "Queen", None), self._testee()._parse_title_artist_target("spiel Show must go on von Queen"))
        self.assertEqual(("Show must go on", "Queen", None), self._testee()._parse_title_artist_target("spiele Show must go on von Queen"))
        self.assertEqual(("Show must go on", "Queen", None), self._testee()._parse_title_artist_target("spiel Show must go on von Queen."))
        self.assertEqual((None, "Queen", None), self._testee()._parse_title_artist_target("spiele etwas von Queen"))
        self.assertEqual((None, "Queen", None), self._testee()._parse_title_artist_target("spiele was von Queen"))
        self.assertEqual((None, "Rammstein", None), self._testee()._parse_title_artist_target("spiele was von Rammstein."))
        self.assertEqual((None, "Rammstein", None), self._testee()._parse_title_artist_target("Spiele was von Rammstein "))

