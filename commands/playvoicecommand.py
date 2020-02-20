#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .voicecommand import ConfigurableVoiceCommand
from .process_result import ProcessResult

class PlayVoiceCommand(ConfigurableVoiceCommand):
    
    SIGNAL_WORDS = ["spiele", "spiel"]
    ARTIST_ONLY = ["etwas", "was"]
    ARTIST = "von"
    TARGET = "auf"
    STRIP_CHARS = ";,. "
    
    def _load_config(self, data):
        self.RENDERERS = data['renderers']
        self.SERVERS = data['servers']
            
    def _get_server_url(self, name):
        # ignore name as there is only one :)
        return next(iter(self.SERVERS.values()))
        
    def _get_renderer_url(self, name):
        if (name is not None) and (name in self.RENDERERS):
            return self.RENDERERS[name]
        return next(iter(self.RENDERERS.values()))
                
    def can_process(self, vc):
        for k in self.SIGNAL_WORDS:
            if vc.lower().startswith(k):
                return True
        return False
        
    def _parse_title_artist_target(self, vc):
        title = None
        artist = None
        target = None
        artist_contained = False

        rest = vc.strip(self.STRIP_CHARS)
        # cut away signal word: rest is like SINGAL_WORD...
        for k in self.SIGNAL_WORDS:
            if k in rest.lower():
                rest = rest[len(k):].strip()
                
        # cut away artist: rest is like <title>ARTIST...
        if self.ARTIST in rest.lower():
            artist_keyword_idx = rest.lower().find(self.ARTIST)
            title = rest[:artist_keyword_idx].strip()
            rest = rest[artist_keyword_idx + len(self.ARTIST):]
            log("artist contained")
            artist_contained = True
        
        # cut away target: rest is like: <artist>TARGET... or <title>TARGET...
        if self.TARGET in rest.lower():
            target_keyword_idx = rest.lower().find(self.TARGET)
            if (title is None):
                title = rest[:target_keyword_idx].strip()
            else:
                artist = rest[:target_keyword_idx].strip()
            target = rest[target_keyword_idx + len(self.ARTIST):].strip()
            log("target contained")
            
        if (title is None):
            # parse artist anyway
            title = rest.strip()
        if (artist_contained and artist is None):
            artist = rest.strip()
            
        # case someone say's "spiel(e) (et)was von ARTIST"
        if title.lower() in self.ARTIST_ONLY:
            title = None

        log('title: "{t}", artist: "{a}", target: "{tt}"'.format(t=title, a=artist, tt=target))
        return (title, artist, target)
        
    def process(self, vc):
        ti, ar, tar = self._parse_title_artist_target(vc)
        from dlna.mediaserver import MediaServer
        from dlna.renderer import Renderer
        from dlna.player import Player
        
        ms_url = self._get_server_url(None)
        ms = MediaServer(ms_url)
        log('searching for title="{t}" of artist="{a}"'.format(t=ti, a=ar))
        search_res = ms.search(title=ti, artist=ar)
        log('Found {} items'.format(search_res.get_matches()))
        
        succ = False
        result_text = ""
        if (search_res.get_matches() > 0):
            item = search_res.random_item()
            log(item.get_url())
            renderer_url = self._get_renderer_url(tar)
            player = Player(Renderer(tar, renderer_url, True))
            log('Playername: "{p}", Player URL: "{u}"'.format(p=tar, u=renderer_url))
            player.play(item.get_url(), item=item)
            succ = True
            result_text = 'spielt "{t}" von "{a}"'.format(t=item.get_title(), a=item.get_actor())
        else:
            succ = False
            result_text = "Kein passenden Titel gefunden"
        log(result_text)
        return ProcessResult("Media Player", succ, result_text)
        
def log(txt):
    pass
        