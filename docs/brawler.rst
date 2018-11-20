Brawler
=======

Returns a brawler object with the following attributes. You can retrieve
a profile’s brawler info by getting `Profile`_.brawlers

.. code:: py

   brawlers = profile.brawlers
   top_brawler = brawlers[0] # first index in list = highest trophies
   print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

Attributes
~~~~~~~~~~

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

.. _Profile: https://github.com/SharpBit/brawlstats/blob/master/docs/profile.md