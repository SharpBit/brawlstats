from box import Box, BoxList

from .utils import bstag

__all__ = ['Player', 'Club', 'Members', 'Ranking', 'BattleLog', 'Constants', 'Brawlers', 'EventRotation']


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
            raise IndexError(f'No such index: {item}')


class BaseBoxList(BaseBox):
    def from_data(self, data):
        self.raw_data = data
        self._boxed_data = BoxList(data, camel_killer_box=True)
        return self

    def __len__(self):
        return sum(1 for i in self)


class Members(BaseBoxList):
    """A list of the members in a club."""

    def __init__(self, client, data):
        super().__init__(client, data['items'])

    def __repr__(self):
        return f'<Members object count={len(self)}>'


class BattleLog(BaseBoxList):
    """A player battle object with all of its attributes."""

    def __init__(self, client, data):
        super().__init__(client, data['items'])


class Club(BaseBox):
    """A club object with all of its attributes."""

    def __repr__(self):
        return f"<Club object name='{self.name}' tag='{self.tag}'>"

    def __str__(self):
        return f'{self.name} ({self.tag})'

    def get_members(self) -> Members:
        """Gets the members of a club.
        Note: It is preferred to get the members
        via Club.members since this method makes
        an extra API call but returns the same data.

        Returns
        -------
        Members
            A list of the members in a club.
        """
        url = f'{self.client.api.CLUB}/{bstag(self.tag)}/members'
        return self.client._get_model(url, model=Members)


class Player(BaseBox):
    """A player object with all of its attributes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_victories = self.x3vs3_victories

    def __repr__(self):
        return f"<Player object name='{self.name}' tag='{self.tag}'>"

    def __str__(self):
        return f'{self.name} ({self.tag})'

    def get_club(self) -> Club:
        """Gets the player's club.

        Returns
        -------
        Club or None
            A list of the members in a club, or None if the player is not in a club.
        """
        if not self.club:
            if self.client.is_async:
                async def wrapper():
                    return None
                return wrapper()
            return None

        url = f'{self.client.api.CLUB}/{bstag(self.club.tag)}'
        return self.client._get_model(url, model=Club)

    def get_battle_logs(self) -> BattleLog:
        """Gets the player's battle logs.

        Returns
        -------
        BattleLog
            The battle log containing the player's most recent battles.
        """
        url = f'{self.client.api.PROFILE}/{bstag(self.tag)}/battlelog'
        return self.client._get_model(url, model=BattleLog)


class Ranking(BaseBoxList):
    """A player or club ranking that contains a list of players or clubs."""

    def __init__(self, client, data):
        super().__init__(client, data['items'])

    def __repr__(self):
        return '<Ranking object count={}>'.format(len(self))


class Constants(BaseBox):
    """Data containing some Brawl Stars constants."""
    pass


class Brawlers(BaseBoxList):
    """A list of available brawlers and information about them."""

    def __init__(self, client, data):
        super().__init__(client, data['items'])


class EventRotation(BaseBoxList):
    """A list of events in the current rotation."""
    pass
