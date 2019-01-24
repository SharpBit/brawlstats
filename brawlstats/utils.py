class API:
    def __init__(self, base_url):
        self.base = base_url or 'https://brawlapi.cf/api'
        self.profile = self.base + '/player'
        self.club = self.base + '/club'
        self.leaderboard = self.base + '/leaderboards'
        self.events = self.base + '/events'
        self.misc = self.base + '/misc'
        self.club_seach = self.base + '/club/search'
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
            'spike',
            'crow',
            'leon'
        ]
