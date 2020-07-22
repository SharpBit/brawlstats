import inspect
import os
import re
from datetime import datetime
from functools import wraps

from .errors import NotFoundError


class API:
    def __init__(self, base_url, version=1):
        self.BASE = base_url or 'https://api.brawlstars.com/v{}'.format(version)
        self.PROFILE = self.BASE + '/players'
        self.CLUB = self.BASE + '/clubs'
        self.RANKINGS = self.BASE + '/rankings'
        # self.CONSTANTS = 'https://fourjr.herokuapp.com/bs/constants'
        self.BRAWLERS = self.BASE + '/brawlers'

        # Get package version from __init__.py
        path = os.path.dirname(__file__)
        with open(os.path.join(path, '__init__.py')) as f:
            self.VERSION = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

        # development:
        self.CURRENT_BRAWLERS = {}

    def set_brawlers(self, brawlers):
        self.CURRENT_BRAWLERS = {b['name'].lower(): int(b['id']) for b in brawlers}
        print(self.CURRENT_BRAWLERS)


def bstag(tag):
    tag = tag.strip('#').upper().replace('O', '0')
    allowed = '0289PYLQGRJCUV'

    if len(tag) < 3:
        raise NotFoundError(404, reason='Tag less than 3 characters.')
    invalid = [c for c in tag if c not in allowed]
    if invalid:
        raise NotFoundError(404, invalid_chars=invalid)

    if not tag.startswith('%23'):
        tag = '%23' + tag

    return tag


def get_datetime(timestamp: str, unix=True):
    """
    Converts a %Y%m%dT%H%M%S.%fZ to a UNIX timestamp
    or a datetime.datetime object

    Parameters
    ----------
    timestamp: str
        A timestamp in the %Y-%m-%dT%H:%M:%S.%fZ format, usually returned by the API
        in the ``created_time`` field for example (eg. 2018-07-18T14:59:06.000Z)
    unix: Optional[bool] = True
        Whether to return a POSIX timestamp (seconds since epoch) or not

    Returns Union[int, datetime.datetime]
    """
    time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    if unix:
        return int(time.timestamp())
    else:
        return time


def nothing(value):
    """Function that returns the argument"""
    return value


def typecasted(func):
    """Decorator that converts arguments via annotations.
    Source: https://github.com/cgrok/clashroyale/blob/master/clashroyale/official_api/utils.py#L11"""
    signature = inspect.signature(func).parameters.items()

    @wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        new_args = []
        new_kwargs = {}
        for _, param in signature:
            converter = param.annotation
            if converter is inspect._empty:
                converter = nothing
            if param.kind is param.POSITIONAL_OR_KEYWORD:
                if args:
                    to_conv = args.pop(0)
                    new_args.append(converter(to_conv))
            elif param.kind is param.VAR_POSITIONAL:
                for a in args:
                    new_args.append(converter(a))
            else:
                for k, v in kwargs.items():
                    nk, nv = converter(k, v)
                    new_kwargs[nk] = nv
        return func(*new_args, **new_kwargs)
    return wrapper


def find_brawler(brawlers, pattern, match):
    """
    Find first match brawler containing template

    Parameters
    ----------
    brawlers: Brawlers
        Brawlers instance

    pattern: Any, usually str or int
        `match` value to find in brawlers

    match: Any, usually str or int
        key by which the search will be performed

    Returns brawler object
    """
    for brawler in brawlers:
        if brawler.get(pattern) == match:
            return brawler
    return None  # returns explicitly
