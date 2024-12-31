from re import Match, compile, Pattern, VERBOSE, IGNORECASE
from dataclasses import dataclass
from collections import namedtuple
import json
from urllib.request import urlopen, Request

from commands.voicecommand import ConfigurableVoiceCommand
from commands.process_result import ProcessResult

TARGET_REST = namedtuple("Target", ["target", "rest"])
TITLE_ARTIST_TARGET = namedtuple("TitleArtistTarget", ["title", "artist", "target"])


@dataclass
class DetectedCommand():
    artist: str = None
    title: str = None
    target: str = None
    loop: bool = False


class PlayVoiceCommand(ConfigurableVoiceCommand):

    SIGNAL_WORDS = ["spiele", "spiel"]
    STRIP_CHARS = ";,. "

    ARTIST = "von"
    TITLE = "mit"
    # where to play
    TARGET = "auf"

    media_controller_url: str

    def _load_config(self, data):
        self.media_controller_url = data['media_controller_url']

    def can_process(self, vc):
        for k in self.SIGNAL_WORDS:
            if vc.lower().startswith(k):
                return True
        return False

    def _find_target(self, txt: str) -> TARGET_REST:
        if self.TARGET in txt:
            target_idx = txt.lower().find(self.TARGET)
            rest = txt[:target_idx]
            target = txt[target_idx + len(self.TARGET):]
            return TARGET_REST(target, rest)
        else:
            return TARGET_REST(None, txt)

    def _parse_rest(self, rest: str, artist_first: bool) -> TITLE_ARTIST_TARGET:
        title = None
        artist = None
        target = None
        keyword_contained = False

        keyword = self.TITLE if artist_first else self.ARTIST

        if keyword in rest.lower():
            keyword_contained = True
            keyword_idx = rest.lower().find(keyword)
            before_keyword = rest[:keyword_idx]
            keyword_value_or_target = self._find_target(before_keyword)
            target = keyword_value_or_target.target
            if artist_first:
                artist = keyword_value_or_target.rest
            else:
                title = keyword_value_or_target.rest
            rest = rest[keyword_idx + len(self.TITLE):]

        if self.TARGET in rest.lower():
            target_keyword_idx = rest.lower().find(self.TARGET)
            target = rest[target_keyword_idx + len(self.TARGET):]
            rest = rest[:target_keyword_idx]

        if keyword_contained:
            if artist_first:
                title = rest
            else:
                artist = rest

        if (not artist_first and title is None):
            title = rest
        if (artist_first and artist is None):
            artist = rest

        # remove spaces, etc.
        if title:
            title = title.strip()
        if artist:
            artist = artist.strip()
        if target:
            target = target.strip()

        return TITLE_ARTIST_TARGET(title=title, artist=artist, target=target)

    SINGLE_PATTERN: Pattern = compile(r"""
    (spiele?)                                           # signal word
    (\s+mir)?                                           # optional mir
    (?:
    (?P<s1>\s+(?:(lied)|(song)|(das\s+lied)|(den\s+song)))|                 # P<rest> is title
    (?P<s2>\s+(?:(ein\s+lied)|(ein\s+song)|(einen\s+song)|(etwas)|(was)))|  # P<rest> is unkonwn
    (?P<loop>\s+(?:(Lieder)|(Songs)))
    )?
    (?:\s+(?:(?P<von>von)|(?P<mit>mit)))?               # P<rest> is artist or title (regardless of previous)
    (?:(?P<rest>(?:(\s+\w+)+)))                         # rest what to play
    """, VERBOSE | IGNORECASE)                          # allowes these comments, ignore case

    def _parse(self, vc: str) -> DetectedCommand:
        txt: str = vc.strip(self.STRIP_CHARS)

        # helper variables
        rest_starts_with_title = True  # meaning rest is artist
        rest_starts_with_artist = False
        loop = False

        m: Match = self.SINGLE_PATTERN.match(txt)
        if not m:
            return False
        if not m.group('rest'):
            return False

        if m.group('s1'):
            rest_starts_with_title = True
        if m.group('mit'):
            rest_starts_with_title = True
        if m.group('von'):
            rest_starts_with_title = False
            rest_starts_with_artist = True
        if m.group('loop'):
            loop = True

        rest_stripped = m.group('rest').strip()
        tat: TITLE_ARTIST_TARGET = None
        if rest_starts_with_title:
            tat = self._parse_rest(rest_stripped, False)
        elif rest_starts_with_artist:
            tat = self._parse_rest(rest_stripped, True)
        else:
            raise ValueError('Whoopsy artist or title?')

        return DetectedCommand(artist=tat.artist, title=tat.title, target=tat.target, loop=loop)

    def _send_to_mediacontroller(self, command: DetectedCommand):
        data = json.dumps(command.__dict__).encode('utf-8')
        req = Request(self.media_controller_url + '/play', data, {"Content-Type": "application/json"})
        return urlopen(req)

    def process(self, vc) -> ProcessResult:
        com = self._parse(vc)

        if (not com):
            return None

        try:
            response = self._send_to_mediacontroller(com)
            response_data = json.loads(response.read())
            description = response_data.get('description', None)
            running = response_data.get('running', None)
            return ProcessResult("Media Player", running, description)
        except Exception as e:
            return ProcessResult("Media Player", False, "Fehler", e)


def log(txt):
    pass
