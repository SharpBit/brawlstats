class API:
    def __init__(self, base_url):
        self.base = base_url or 'https://brawlapi.cf/api'
        self.profile = self.base + '/players'
        self.club = self.base + '/clubs'
        self.leaderboard = self.base + '/leaderboards'
        self.events = self.base + '/events'
        self.misc = self.base + '/misc'
        self.club_seach = self.base + '/clubSearch'
        self.constants = 'https://fourjr.herokuapp.com/bs/constants/'
