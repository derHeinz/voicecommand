#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import quote
from urllib.request import urlopen, Request
import json

from .voicecommand import ConfigurableVoiceCommand
from .process_result import ProcessResult

class PlayYoutubeVoiceCommand(ConfigurableVoiceCommand):

    SIGNAL_WORDS = ["youtube spiele", "youtube spiel"]
    STRIP_CHARS = ";,. "
    
    def _load_config(self, data):
        self.RENDERERS = data['renderers']
        self.provider_url = data['youtube_audio_provider_url']
        
    def _get_renderer_url(self, name):
        if (name is not None) and (name in self.RENDERERS):
            return self.RENDERERS[name]
        return next(iter(self.RENDERERS.values()))

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
        header = {"Content-Type":"text/plain"}
        req = Request(url, None, header)
        path_to_audiofile = urlopen(req).read() # will download and return url to the audio file as plaintext
        
        path_to_audiofile = path_to_audiofile.decode('UTF-8')
        path_to_audiofile = path_to_audiofile.strip() # remove trailing line feed

        escaped_path_to_audiofile = quote(path_to_audiofile)
        return baseurl + escaped_path_to_audiofile

    def _get_audio_info(self, baseurl, searchquery):
        searchquery_escaped = quote(searchquery)
        url = baseurl + '/searchv2/' + searchquery_escaped
        header = {"Content-Type":"text/plain"}
        req = Request(url, None, header)
        call_result = urlopen(req).read() # will download and return info including url to the audio file
        json_result = json.loads(call_result.decode('UTF-8'))
        
        info = json_result
        info['absolutePath'] = baseurl + quote(json_result['path'])

        return info
        
    def process(self, vc):
        search_query = self._extract_search_query(vc)
        
        # old way
        #audio_url = self._get_audio_file(self.provider_url, search_query)
        info = self._get_audio_info(self.provider_url, search_query)
        audio_url = info['absolutePath']

        message = None
        if (info.get('title', None) != None):
            message = "Spielt %s" % info['title']
        else:
            message = "Spielt Datei %s" % info['filename'] 
        
        # make a DLNA player and player
        from dlna.dlna.renderer import Renderer
        from dlna.dlna.player import Player
        
        target_name = None
        renderer_url = self._get_renderer_url(target_name)
        player = Player(Renderer(target_name, renderer_url, False))
        
        player.play(audio_url)
        
        return ProcessResult("Youtube Media Player", True, message)
        