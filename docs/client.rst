Client
======

This is an async, easy to use, and clean client to get Brawl Stars
statistics.

Initialization
~~~~~~~~~~~~~~

Import brawlstats and create the client like so:

.. code:: py

   import brawlstats

   client = brawlstats.Client('token', timeout=3)

Note: Do not put your API key on a public github repo.

Parameters
~~~~~~~~~~

========== ======= =======================
Name       Type    Default
========== ======= =======================
token      str     **Required**
\**timeout int     5
\**session session aiohttp.ClientSession()
\**loop    loop    None
========== ======= =======================

Get your token by typing ``.getToken`` in the `Discord Server`_.

Methods
~~~~~~~

| * ``get_profile``\
| tag-\ ``str`` A valid player tag
| Returns: `Profile`_\
| * ``get_band``\
| tag-\ ``str`` A valid player tag
| full-\ ``bool`` Default = ``False``
| Returns: `Band`_ if ``full`` is ``True`` else `SimpleBand`_ or ``None`` if no band.
| ``get_leaderboard``\
| p_or_b-\ ``str`` Must be 'players' or 'bands' or else it will return a ``ValueError``\
| count-\ ``int`` The number of players/bands to get.
| Returns: List[\ `LBPlayer`_, `LBPlayer`_] or List[\ `LBBand`_, `LBBand`_]

.. _Discord Server: https://discord.me/BrawlAPI
.. _Profile: https://github.com/SharpBit/brawlstats/blob/master/docs/profile.rst
.. _Band: https://github.com/SharpBit/brawlstats/blob/master/docs/band.rst
.. _SimpleBand: https://github.com/SharpBit/brawlstats/blob/master/docs/band.rst#simpleband
.. _LBPlayer: https://github.com/SharpBit/brawlstats/master/docs/leaderboard.rst#player
.. _LBBand: https://github.com/SharpBit/brawlstats/master/docs/leaderboard.rst#band