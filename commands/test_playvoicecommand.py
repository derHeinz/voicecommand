import unittest
from .playvoicecommand import PlayVoiceCommand, DetectedCommand
from unittest.mock import patch, MagicMock


class TestPlayVoiceCommand(unittest.TestCase):

    def _testee(sef):
        return PlayVoiceCommand({"media_controller_url": "url"})

    def test_can_process(self):
        positive_list = ["spiele Lied", "spiel Heavy von Queen", "spiel Bohemian", "spiele eine Lied", 
                         "Spiele etwas von Queen.", "spiel Show must go on.", "spiel Show must go on "]
        for text in positive_list:
            self.assertTrue(self._testee().can_process(text))

        negative_list = ["etwas ist passiert", "mache Licht an", "Fernseher aus", "Spotify spiele Titel"]
        for text in negative_list:
            self.assertFalse(self._testee().can_process(text))

    def _check_detected_command(self, dc: DetectedCommand, artist: str = None, title: str = None,
                                loop: bool = False, target: str = None):
        self.assertEqual(artist, dc.artist)
        self.assertEqual(title, dc.title)
        self.assertEqual(loop, dc.loop)
        self.assertEqual(target, dc.target)

    @patch('commands.playvoicecommand.Request')
    @patch('commands.playvoicecommand.urlopen')
    def test_send_to_mediacontroller(self, mock_urlopen, request_mock):

        self._testee()._send_to_mediacontroller(DetectedCommand('asfd'))
        request_mock.assert_called_with('url/play', '{"artist": "asfd", "title": null, "target": null, "loop": false}'
                                        .encode('utf-8'),
                                        {'Content-Type': 'application/json'})
        mock_urlopen.assert_called()

        request_mock.reset_mock()
        mock_urlopen.reset_mock()
        self._testee()._send_to_mediacontroller(DetectedCommand(title='foo', artist='bar', loop=True))
        request_mock.assert_called_with('url/play', '{"artist": "bar", "title": "foo", "target": null, "loop": true}'
                                        .encode('utf-8'),
                                        {'Content-Type': 'application/json'})
        mock_urlopen.assert_called()

    @patch('commands.playvoicecommand.Request')
    @patch('commands.playvoicecommand.urlopen')
    def test_process(self, mock_urlopen, request_mock):
        resp = MagicMock()
        resp.read.return_value = '{"running": true, "description": "Spielt ein tolles Lied einer sagenhaften Band"}'
        mock_urlopen.return_value = resp

        pr = self._testee().process('Spiele Show must go on von Queen auf Radio')

        request_mock.assert_called_with('url/play',
                                        '{"artist": "Queen", "title": "Show must go on", "target": "Radio", "loop": false}'
                                        .encode('utf-8'),
                                        {'Content-Type': 'application/json'})
        mock_urlopen.assert_called()
        self.assertEqual(pr.get_message(), "Spielt ein tolles Lied einer sagenhaften Band")
        self.assertEqual(pr.get_type(), "Media Player")
        self.assertEqual(True, pr.is_sucess())

    def test_parse_rest(self):
        self.assertEqual(("Hammer", None, None), self._testee()._parse_rest("Hammer", False))
        self.assertEqual(("Hammer", "Queen", "Radio"), self._testee()._parse_rest("Hammer von Queen auf Radio", False))
        self.assertEqual(("Hammer", "Queen", None), self._testee()._parse_rest("Hammer von Queen", False))
        self.assertEqual(("Hammer", None, "Radio"), self._testee()._parse_rest("Hammer auf Radio", False))
        self.assertEqual(("Hammer", "Queen", "Radio"), self._testee()._parse_rest("Hammer auf Radio von Queen", False))

        self.assertEqual((None, "Queen", None), self._testee()._parse_rest("Queen", True))
        self.assertEqual((None, "Queen", "Radio"), self._testee()._parse_rest("Queen auf Radio", True))
        self.assertEqual(("Hammer", "Queen", "Radio"), self._testee()._parse_rest("Queen auf Radio mit Hammer", True))
        self.assertEqual(("Hammer", "Queen", None), self._testee()._parse_rest("Queen mit Hammer", True))
        self.assertEqual(("Hammer", "Queen", "Radio"), self._testee()._parse_rest("Queen mit Hammer auf Radio", True))       

    def test_parse_single_song_title(self):
        self._check_detected_command(self._testee()._parse("spiel Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele Show must go on;"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("Spiele Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele Lied Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele Song Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiel     Lied        Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele das Lied Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele den Song Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("spiele mir den Song Show must go on"), title="Show must go on")
        # mit
        self._check_detected_command(self._testee()._parse("Spiele mir den Song mit Show must go on"), title="Show must go on")
        self._check_detected_command(self._testee()._parse("Spiele das Lied    mit Show must go on"), title="Show must go on")

    def test_parse_single_song_artist(self):
        self._check_detected_command(self._testee()._parse("spiel etwas von Queen"), artist="Queen")
        self._check_detected_command(self._testee()._parse("spiel mir was von Queen"), artist="Queen")
        self._check_detected_command(self._testee()._parse("Spiel    MIR    Was     Von    Queen"), artist="Queen")
        self._check_detected_command(self._testee()._parse("spiel mir ein Lied von Queen"), artist="Queen")
        self._check_detected_command(self._testee()._parse("spiel einen Song von Queen"), artist="Queen")

    def test_parse_single(self):
        # title first
        self._check_detected_command(self._testee()._parse("spiel Show must go on von Queen auf Radio Wohnzimmer"),
                                     title="Show must go on", artist="Queen", target="Radio Wohnzimmer")
        self._check_detected_command(self._testee()._parse("spiel Show must go on von Queen"),
                                     title="Show must go on", artist="Queen")
        self._check_detected_command(self._testee()._parse("spiel Show must go on auf Radio Wohnzimmer"),
                                     title="Show must go on", target="Radio Wohnzimmer")
        # artist first
        self._check_detected_command(self._testee()._parse("spiel etwas von Queen auf Radio Wohnzimmer"),
                                     title=None, artist="Queen", target="Radio Wohnzimmer")
        self._check_detected_command(self._testee()._parse("spiel mir was von Queen auf Radio"),
                                     artist="Queen", target="Radio")

    def test_parse_multiple(self):
        self._check_detected_command(self._testee()._parse("spiele Lieder von Queen"),
                                     artist="Queen", loop=True)
        self._check_detected_command(self._testee()._parse("spiele Songs von Queen mit Hammer"),
                                     title="Hammer", artist="Queen", loop=True)
        self._check_detected_command(self._testee()._parse("spiele Songs von Queen mit Hammer auf Radio"),
                                     title="Hammer", artist="Queen", target="Radio", loop=True)
