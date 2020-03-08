import inspect
import json
import os
import re
import urllib.request
from functools import wraps

from ..errors import NotFoundError


class API:
    def __init__(self, base_url, version=1):
        self.BASE = base_url or 'https://api.starlist.pro/v{}'.format(version)
        self.PROFILE = self.BASE + '/player'
        self.CLUB = self.BASE + '/club'
        self.LEADERBOARD = self.BASE + '/leaderboards'
        self.EVENTS = self.BASE + '/events'
        self.MISC = self.BASE + '/misc'
        self.BATTLELOG = self.PROFILE + '/battlelog'
        self.CLUB_SEARCH = self.CLUB + '/search'
        self.CONSTANTS = 'https://fourjr.herokuapp.com/bs/constants'

        # Get package version from __init__.py
        path = os.path.join(os.path.dirname(__file__), os.path.pardir)
        with open(os.path.join(path, '__init__.py')) as f:
            self.VERSION = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

        # Get current brawlers and their IDs
        try:
            data = json.loads(urllib.request.urlopen(self.CONSTANTS + '/characters').read())
        except (TypeError, urllib.error.HTTPError, urllib.error.URLError):
            self.BRAWLERS = {}
        else:
            if data:
                self.BRAWLERS = {
                    b['tID'].lower(): str(b['scId'])[:2] + '0' + str(b['scId'])[2:]
                    for b in data if b['tID']
                }
            else:
                self.BRAWLERS = {}


def bstag(tag):
    tag = tag.strip('#').upper().replace('O', '0')
    allowed = '0289PYLQGRJCUV'
    print(tag)
    if len(tag) < 3:
        print(f'Less than 3 {tag}')
        raise NotFoundError('Tag less than 3 characters.', 404)
    invalid = [c for c in tag if c not in allowed]
    if invalid:
        raise NotFoundError(404, invalid)
    return tag

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
                converter = lambda a: a  # do nothing
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
