from urllib.parse import quote
from urllib.request import urlopen, Request
import json

from commands.voicecommand import ConfigurableVoiceCommand
from commands.process_result import ProcessResult


class PlayYoutubeVoiceCommand(ConfigurableVoiceCommand):

    SIGNAL_WORDS = ["youtube spiele", "youtube spiel"]
    STRIP_CHARS = ";,. "

    media_controller_url: str

    def _load_config(self, data):
        self.media_controller_url = data['media_controller_url']
        self.provider_url = data['youtube_audio_provider_url']

    def can_process(self, vc):
        for k in self.SIGNAL_WORDS:
            if vc.lower().startswith(k):
                return True
        return False

    def _extract_search_query(self, vc):
        rest = vc.strip(self.STRIP_CHARS)

        for k in self.SIGNAL_WORDS:
            if rest.lower().startswith(k):
                rest = rest[len(k):].strip()
        return rest

    def _get_audio_file(self, baseurl, searchquery):
        searchquery_escaped = quote(searchquery)
        url = baseurl + '/search/' + searchquery_escaped
        header = {"Content-Type": "text/plain"}
        req = Request(url, None, header)
        path_to_audiofile = urlopen(req).read()  # will download and return url to the audio file as plaintext

        path_to_audiofile = path_to_audiofile.decode('UTF-8')
        path_to_audiofile = path_to_audiofile.strip()  # remove trailing line feed

        escaped_path_to_audiofile = quote(path_to_audiofile)
        return baseurl + escaped_path_to_audiofile

    def _get_audio_info(self, baseurl, searchquery):
        searchquery_escaped = quote(searchquery)
        url = baseurl + '/searchv2/' + searchquery_escaped
        header = {"Content-Type": "text/plain"}
        req = Request(url, None, header)
        call_result = urlopen(req).read()  # will download and return info including url to the audio file
        json_result = json.loads(call_result.decode('UTF-8'))

        info = json_result
        info['absolutePath'] = baseurl + quote(json_result['path'])

        return info

    def _send_to_mediacontroller(self, url: str):
        data = {
            "url": url
        }
        data_encoded = json.dumps(data).encode('utf-8')
        req = Request(self.media_controller_url + '/play', data_encoded, {"Content-Type": "application/json"})
        return urlopen(req)

    def process(self, vc):
        search_query = self._extract_search_query(vc)

        info = self._get_audio_info(self.provider_url, search_query)
        audio_url = info['absolutePath']

        message = None
        if (info.get('title', None) is not None):
            message = "Spielt %s" % info['title']
        else:
            message = "Spielt Datei %s" % info['filename']

        try:
            response = self._send_to_mediacontroller(audio_url)
            response_data = json.loads(response.read())
            if response_data.get('running', None):
                return ProcessResult("Youtube Media Player", True, message)
            else:
                return ProcessResult("Youtube Media Player", False, "Fehler beim Abspielen")
        except Exception:
            return ProcessResult("Youtube Media Player", False, "Fehler beim Suchen")
