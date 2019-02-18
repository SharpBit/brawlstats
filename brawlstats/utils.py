from .errors import NotFoundError


class API:
    def __init__(self, base_url):
        self.base = base_url or 'https://brawlapi.cf/api'
        self.profile = self.base + '/player'
        self.club = self.base + '/club'
        self.leaderboard = self.base + '/leaderboards'
        self.events = self.base + '/events'
        self.misc = self.base + '/misc'
        self.club_search = self.base + '/club/search'
        self.constants = 'https://fourjr.herokuapp.com/bs/constants/'
        self.brawlers = [
            'shelly',
            'nita',
            'colt',
            'bull',
            'jessie',
            'brock',
            'dynamike',
            'bo',
            'el primo',
            'barley',
            'poco',
            'ricochet',
            'penny',
            'darryl',
            'frank',
            'pam',
            'piper',
            'mortis',
            'tara',
            'gene',
            'spike',
            'crow',
            'leon'
        ]


def bstag(tag):
    tag = tag.strip('#').upper().replace('O', '0')
    allowed = '0289PYLQGRJCUV'
    if len(tag) < 3:
        raise NotFoundError('Tag less than 3 characters.', 404)
    invalid = [c for c in tag if c not in allowed]
    if invalid:
        raise NotFoundError(invalid, 404)
    return tag
