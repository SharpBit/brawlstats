from box import Box, BoxList


class BaseBox:
    def __init__(self, client, resp, data):
        self.client = client
        self.resp = resp
        self.from_data(data)

    def from_data(self, data):
        self.raw_data = data
        if isinstance(data, list):
            self._boxed_data = BoxList(
                data, camel_killer_box=True
            )
        else:
            self._boxed_data = Box(
                data, camel_killer_box=True
            )
        return self

    def __getattr__(self, attr):
        try:
            return getattr(self._boxed_data, attr)
        except AttributeError:
            try:
                return super().__getattr__(attr)
            except AttributeError:
                return None  # users can use an if statement rather than try/except to find a missing attribute

    def __getitem__(self, item):
        try:
            return self._boxed_data[item]
        except IndexError:
            raise IndexError('No such index: {}'.format(item))


class Player(BaseBox):
    """
    Returns a full player object with all of its attributes.
    """

    def __repr__(self):
        return "<Player object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_club(self, full=True):
        """
        Gets the player's club.

        Parameters
        ----------
        full: Optional[bool] = True
            Whether or not to get the player's full club stats or not.

        Returns None, PartialClub, or Club
        """
        if not self.club:
            return None
        if full:
            club = self.client.get_club(self.club.tag)
        else:
            club = PartialClub(self.client, self.resp, self.club)
        return club


class PartialClub(BaseBox):
    """
    Returns a simple club object with some of its attributes.
    """

    def __repr__(self):
        return "<PartialClub object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_full(self):
        """
        Gets the full club statistics.

        Returns Club
        """
        return self.client.get_club(self.tag)


class Club(BaseBox):
    """
    Returns a full club object with all of its attributes.
    """

    def __repr__(self):
        return "<Club object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)


class Leaderboard(BaseBox):
    """
    Returns a player or club leaderboard that contains a list of players or clubs.
    """

    def __len__(self):
        return sum(1 for i in self)

    def __repr__(self):
        return "<Leaderboard object count={}>".format(len(self))

    def __str__(self):
        return 'Leaderboard containing {} items'.format(len(self))

class Events(BaseBox):
    """
    Returns current and upcoming events.
    """
    pass


class Constants(BaseBox):
    """
    Returns some Brawl Stars constants.
    """
    pass


class MiscData(BaseBox):
    """
    Misc data such as shop and season info.
    """
    pass
