from box import Box, BoxList
from .utils import bstag


__all__ = ['Player', 'Club', 'Members', 'Ranking', 'BattleLog', 'Constants', 'Brawlers']


class BaseBox:
    def __init__(self, client, data):
        self.client = client
        self.from_data(data)

    def from_data(self, data):
        self.raw_data = data
        self._boxed_data = Box(data, camel_killer_box=True)
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


class BaseBoxList(BaseBox):
    def from_data(self, data):
        data = data['items']
        self.raw_data = data
        self._boxed_data = BoxList(data, camel_killer_box=True)
        return self

    def __len__(self):
        return sum(1 for i in self)


class Player(BaseBox):
    """
    Returns a full player object with all of its attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_victories = self.x3vs3_victories

    def __repr__(self):
        return "<Player object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} ({0.tag})'.format(self)

    def get_club(self):
        """
        Gets the player's club.

        Returns Optional[Club]
        """
        if not self.club:
            return None
        url = '{}/{}'.format(self.client.api.CLUB, bstag(self.club.tag))
        return self.client._get_model(url, model=Club)


class Club(BaseBox):
    """
    Returns a full club object with all of its attributes.
    """

    def __repr__(self):
        return "<Club object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} ({0.tag})'.format(self)

    def get_members(self):
        """
        Gets the members of a club.

        Returns Members
        """
        url = '{}/{}/members'.format(self.client.api.CLUB, bstag(self.tag))
        return self.client._get_model(url, model=Members)


class Members(BaseBoxList):
    """
    Returns the members in a club.
    """

    def __repr__(self):
        return '<Members object count={}>'.format(len(self))


class Ranking(BaseBoxList):
    """
    Returns a player or club ranking that contains a list of players or clubs.
    """

    def __repr__(self):
        return '<Ranking object count={}>'.format(len(self))


class BattleLog(BaseBoxList):
    """
    Returns a full player battle object with all of its attributes.
    """
    pass


class Constants(BaseBox):
    """
    Returns some Brawl Stars constants.
    """
    pass


class Brawlers(BaseBoxList):
    """
    Returns list of available brawlers and information about them.
    """

    def __repr__(self):
        return '<Brawlers object count={}>'.format(len(self))

    def __str__(self):
        return 'Here {} brawlers'.format(len(self))
