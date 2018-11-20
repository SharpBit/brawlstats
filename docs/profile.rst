Profile
=======

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

Methods
~~~~~~~

``get_band``\  full-\ ``bool``\  Returns: `Band`_ if ``full=True`` else
`SimpleBand`_ or ``None`` if no band. Default=\ ``False``

Attributes
~~~~~~~~~~

=========================== ==============================
Name                        Type
=========================== ==============================
``tag``                     str
``id.high``                 int
``id.low``                  int
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

.. _Band: https://github.com/SharpBit/brawlstats/blob/master/docs/band.md
.. _SimpleBand: https://github.com/SharpBit/brawlstats/blob/master/docs/band.md#simpleband
.. _Brawler: https://github.com/SharpBit/brawlstats/blob/master/docs/brawler.md