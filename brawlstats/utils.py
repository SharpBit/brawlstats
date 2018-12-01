class API:
    def __init__(self, base_url):
        self.base = base_url or 'https://brawlapi.cf/api'
        self.profile = self.base + '/players'
        self.band = self.base + '/bands'
        self.leaderboard = self.base + '/leaderboards'
        self.events = self.base + '/events'
