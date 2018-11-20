Band
====

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

Attributes
~~~~~~~~~~

===================== ============================
Name                  Type
===================== ============================
``tag``               str
``id.high``           int
``id.low``            int
``name``              str
``status``            str
``members_count``     int
``trophies``          int
``required_trophies`` int
``description``       str
``members``           List[\ `Member`_, `Member`_]
===================== ============================

Simple Band
===========

Only returns some statistics of the band. You are returned this via
`Profile`_.band To get a full band, use await `Profile`_.get_band()

.. _attributes-1:

Attributes
~~~~~~~~~~

===================== ====
Name                  Type
===================== ====
``id.high``           int
``id.low``            int
``name``              str
``tag``               str
``role``              str
``trophies``          int
``required_trophies`` int
``members``           int
``badge_id``          int
``online_members``    int
===================== ====

.. _Member: https://github.com/SharpBit/brawlstats/blob/master/docs/member.md
.. _Profile: https://github.com/SharpBit/brawlstats/blob/master/docs/profile.md