from twisted.internet import protocol
from .protocol import Protocol
from ..lib.core import Player
from ..utils import json_dumps, Setting


class Factory(protocol.Factory):
    def __init__(self):
        self.clients = []
        self.doubanfm = Player()
        self.doubanfm.hooks.register({
            'play':            self.on_play,
            'pause':           self.on_pause,
            'resume':          self.on_resume,
            'kbps_change':     self.on_kbps_change,
            'channel_change':  self.on_channel_change,
            'volume_change':   self.on_volume_change,
            'playlist_change': self.on_playlist_change,
            'skip':            self.on_skip,
            'remove':          self.on_remove,
            'like':            self.on_like,
            'unlike':          self.on_unlike,
            'login_success':   self.on_login_success,
            'logout':          self.on_logout,
        })
        self.doubanfm.run()

    def on_play(self):
        self.broadcast('play', self.doubanfm.song)
        print('play: ' + json_dumps(self.doubanfm.song))

    def on_pause(self):
        self.broadcast('pause')
        print('pause')

    def on_resume(self):
        self.broadcast('resume')
        print('resume')

    def on_login_success(self):
        self.broadcast('login_success', self.doubanfm.user)
        print('login success: ' + json_dumps(self.doubanfm.user))

    def on_kbps_change(self):
        self.broadcast('kbps', Setting.get('kbps'))
        print('kbps: %skbps' % Setting.get('kbps'))

    def on_channel_change(self):
        self.broadcast('channel', Setting.get('channel'))
        print('channel: %s' % Setting.get('channel'))

    def on_volume_change(self):
        self.broadcast('volume', self.doubanfm.player.get_volume())
        print('volume: %s' % self.doubanfm.player.get_volume())

    def on_playlist_change(self):
        self.broadcast('playlist', self.doubanfm.playlist)
        print('playlist: %s' % json_dumps(self.doubanfm.playlist))

    def on_skip(self):
        self.broadcast('skip')
        print('skip')

    def on_remove(self):
        self.broadcast('remove')
        print('remove')

    def on_like(self):
        self.broadcast('like')
        print('like')

    def on_unlike(self):
        self.broadcast('unlike')
        print('unlike')

    def on_logout(self):
        self.broadcast('logout')
        print('logout')

    def broadcast(self, *data):
        for client in self.clients:
            client.send(*data)

    def buildProtocol(self, addr):
        return Protocol(self)
