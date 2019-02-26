from .errors import NotFoundError

import re


class API:
    def __init__(self, base_url):
        self.BASE = base_url or 'https://brawlapi.cf/api'
        self.PROFILE = self.BASE + '/player'
        self.CLUB = self.BASE + '/club'
        self.LEADERBOARD = self.BASE + '/leaderboards'
        self.EVENTS = self.BASE + '/events'
        self.MISC = self.BASE + '/misc'
        self.CLUB_SEARCH = self.BASE + '/club/search'
        self.CONSTANTS = 'https://fourjr.herokuapp.com/bs/constants/'
        self.BRAWLERS = [
            'shelly', 'nita', 'colt', 'bull', 'jessie',  # league reward 0-500
            'brock', 'dynamike', 'bo',                   # league reward 1000+
            'el primo', 'barley', 'poco',                # rare
            'ricochet', 'penny', 'darryl',               # super rare
            'frank', 'pam', 'piper',                     # epic
            'mortis', 'tara', 'gene',                    # mythic
            'spike', 'crow', 'leon'                      # legendary
        ]

        with open('../brawlstats/__init__.py') as f:
            self.VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


def bstag(tag):
    tag = tag.strip('#').upper().replace('O', '0')
    allowed = '0289PYLQGRJCUV'
    if len(tag) < 3:
        raise NotFoundError('Tag less than 3 characters.', 404)
    invalid = [c for c in tag if c not in allowed]
    if invalid:
        raise NotFoundError(invalid, 404)
    return tag
