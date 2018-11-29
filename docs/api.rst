API Reference
=============

.. autoclass:: brawlstats.core.Client
    :members:

Data Models
-----------

.. autoclass:: brawlstats.core.Profile
    :members:

.. autoclass:: brawlstats.core.Band
    :members:

.. autoclass:: brawlstats.core.SimpleBand
    :members:

.. autoclass:: brawlstats.core.Leaderboard
    :members:

.. autoclass:: brawlstats.core.Events
    :members:

Profile
-------

A full profile of a player (all its statistics)

.. code:: py

   import brawlstats
   import asyncio

   client = brawlstats.Client('token')
   async def main():
       profile = await client.get_profile('GGJVJLU2') # get a player profile
       print(profile.name) # prints 'SharpBit'

   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())

Attributes:

=========================== ==============================
Name                        Type
=========================== ==============================
``tag``                     str
``name``                    str
``brawlers_unlocked``       int
``brawlers``                List[\ `Brawler`_, `Brawler`_]
``victories``               int
``solo_showdown_victories`` int
``duo_showdown_victories``  int
``total_exp``               int
``trophies``                int
``highest_trophies``        int
``account_age_in_days``     int
``avatar_id``               int
``best_time_as_boss``       str
``best_robo_rumble_time``   str
``has_skins``               bool
``band``                    `SimpleBand`_
=========================== ==============================

Band
----

A full band object to get a band’s statistics. In order to get this, you
must get it from the client or a player object.

.. code:: py

   import brawlstats
   import asyncio

   client = brawlstats.Client('token')
   async def main():
       profile = await client.get_profile('GGJVJLU2') # get a player profile
       band = await profile.get_band(full=True) # full=True avoids a SimpleBand
       # OR
       band = await client.get_band('QCGV8PG')

   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())

Attributes:

===================== ============================
Name                  Type
===================== ============================
``tag``               str
``name``              str
``status``            str
``members_count``     int
``trophies``          int
``required_trophies`` int
``description``       str
``members``           List[\ `Member`_, `Member`_]
===================== ============================

SimpleBand
----------

Only returns some statistics of the band. You are returned this via
`Profile`_.band To get a full band, use await `Profile`_.get_band()


Attributes

===================== ====
Name                  Type
===================== ====
``name``              str
``tag``               str
``role``              str
``trophies``          int
``required_trophies`` int
``members``           int
``badge_id``          int
``online_members``    int
===================== ====

Member
------

Returns some info about a band member. Get this by accessing
`Band`_.members

.. code:: py

   members = band.members
   print(members[0].name, members[0].role) # prints best player's name and role (sorted by trophies)

Attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``role``       str
``exp_level``  int
``trophies``   int
``avatar_id``  int
``avatar_url`` str
============== ====

Leaderboard
-----------

Returns a list of top players or bands. To access this, do ``lb.players[index]`` or ``lb.bands[index]``

Player attributes:

============= ====
Name          Type
============= ====
``tag``       str
``name``      str
``position``  int
``trophies``  int
``band_name`` str
``exp_level`` int
============= ====

Band attributes:

================= ====
Name              Type
================= ====
``tag``           str
``name``          str
``position``      int
``trophies``      int
``members_count`` int
================= ====

Brawler
-------

Returns a brawler object with the following attributes. You can retrieve
a profile’s brawler info by getting `Profile`_.brawlers

.. code:: py

   brawlers = profile.brawlers
   top_brawler = brawlers[0] # first index in list = highest trophies
   print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

Attributes:

==================== =============================
Name                 Type
==================== =============================
``name``             str
``has_skin``         bool
``skin``             None if no skin otherwise str
``trophies``         int
``highest_trophies`` int
``level``            int
==================== =============================

Events
------

Returns a result of current and upcoming events.

Attributes:

============ ===================
Name         Type
============ ===================
``current``  List[\Event, Event]
``upcoming`` List[\Event, Event]
============ ===================

Event Attributes:

================= ====
Name              Type
================= ====
``slot``          int
``timeInSeconds`` int
``mapId``         int
================= ====




.. _Band: https://brawlstats.readthedocs.io/en/latest/api.html#id1
.. _SimpleBand: https://brawlstats.readthedocs.io/en/latest/api.html#id2
.. _Brawler: https://brawlstats.readthedocs.io/en/latest/api.html#id6
.. _Member: https://brawlstats.readthedocs.io/en/latest/api.html#id4
.. _Profile: https://brawlstats.readthedocs.io/en/latest/api.html#profile