import json
import os
import re
import urllib.parse
import urllib.request

from ..errors import NotFoundError


class API:
    def __init__(self, base_url, version=1):
        self.BASE = base_url or 'https://api.brawlstars.com/v{}'.format(version)
        self.PROFILE = self.BASE + '/players'
        self.CLUB = self.BASE + '/clubs'
        self.RANKINGS = self.BASE + '/rankings'
        self.BRAWLERS = self.CLUB + '/brawlers'
        self.CONSTANTS = 'https://fourjr.herokuapp.com/bs/constants/'

        path = os.path.join(os.path.dirname(__file__), os.path.pardir)
        with open(os.path.join(path, '__init__.py')) as f:
            self.VERSION = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

        try:
            data = json.loads(urllib.request.urlopen(self.CONSTANTS).read())
        except (TypeError, urllib.error.HTTPError, urllib.error.URLError):
            self.BRAWLERS = []
        else:
            if data:
                self.BRAWLERS = {b['tID'].lower(): b['scId'] for b in data['characters'] if b['tID']}
            else:
                self.BRAWLERS = []


def bstag(tag):
    tag = tag.strip('#').upper().replace('O', '0')
    allowed = '0289PYLQGRJCUV'
    if len(tag) < 3:
        raise NotFoundError('Tag less than 3 characters.', 404)
    invalid = [c for c in tag if c not in allowed]
    if invalid:
        raise NotFoundError(invalid, 404)
    return urllib.parse.quote('#' + tag)
