API Reference
=============

BrawlAPI
--------

.. autoclass:: brawlstats.BrawlAPI
    :members:

.. autoclass:: brawlstats.brawlapi.core.Client
    :members:

Data Models
~~~~~~~~~~~

.. autoclass:: brawlstats.brawlapi.models.Player
    :members:

.. autoclass:: brawlstats.brawlapi.models.Club
    :members:

.. autoclass:: brawlstats.brawlapi.models.PartialClub
    :members:

.. autoclass:: brawlstats.brawlapi.models.Leaderboard
    :members:

.. autoclass:: brawlstats.brawlapi.models.Events
    :members:

.. autoclass:: brawlstats.brawlapi.models.Constants
    :members:

.. autoclass:: brawlstats.brawlapi.models.MiscData
    :members:

.. autoclass:: brawlstats.brawlapi.models.BattleLog
    :members:

Player
~~~~~~

A full player object (all its statistics)


Attributes:

============================ =======================
Name                         Type
============================ =======================
``tag``                      str
``name``                     str
``name_color_code``          str
``brawlers_unlocked``        int
``brawlers``                 List[\Brawler, Brawler]
``victories``                int
``solo_showdown_victories``  int
``duo_showdown_victories``   int
``total_exp``                int
``exp_level``                int
``exp_fmt``                  str
``trophies``                 int
``highest_trophies``         int
``avatar_id``                int
``avatar_url``               str
``best_time_as_big_brawler`` str
``best_robo_rumble_time``    str
``has_skins``                bool
``club``                     PartialClub
============================ =======================

Club
~~~~

A full club object to get a club's statistics. In order to get this, you
must get it from the client or a player object.


Attributes:

===================== =====================
Name                  Type
===================== =====================
``tag``               str
``name``              str
``status``            str
``members_count``     int
``online_members``    int
``trophies``          int
``required_trophies`` int
``description``       str
``badge_id``          int
``badge_url``         str
``members``           List[\Member, Member]
===================== =====================

PartialClub
~~~~~~~~~~~

Only returns some statistics of the club. You are returned this via
Profile.club To get a full club, use await Profile.get_club()


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
``badge_url``         str
``members``           int
``online_members``    int
===================== ====

Member
~~~~~~

Returns some info about a club member. Get this by accessing
Club.members

.. code:: py

   members = club.members
   print(members[0].name, members[0].role) # prints best player's name and role (sorted by trophies)

Attributes:

=================== ====
Name                Type
=================== ====
``tag``             str
``name``            str
``name_color_code`` str
``role``            str
``trophies``        int
``avatar_id``       int
``avatar_url``      str
=================== ====

Leaderboard
~~~~~~~~~~~

Returns a list of top players, clubs, or brawlers. To access this, do ``lb[index]``

Player attributes:

=================== ====
Name                Type
=================== ====
``tag``             str
``name``            str
``name_color_code`` str
``position``        int
``trophies``        int
``club_name``       str
``exp_level``       int
``avatar_id``       int
``avatar_url``      str
=================== ====

Club attributes:

================= ====
Name              Type
================= ====
``tag``           str
``name``          str
``position``      int
``trophies``      int
``members_count`` int
``badge_id``      int
``badge_url``     str
================= ====

Brawler attributes:

=================== ====
Name                Type
=================== ====
``tag``             str
``name``            str
``name_color_code`` str
``position``        int
``trophies``        int
``club_name``       str
``exp_level``       int
``avatar_id``       int
``avatar_url``      str
``rank``            int
=================== ====

Brawler
~~~~~~~

Returns a brawler object with the following attributes. You can retrieve
a profile’s brawler info by getting Profile.brawlers

.. code:: py

   brawlers = profile.brawlers
   top_brawler = brawlers[0] # first index in list = highest trophies
   print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

Attributes:

==================== ===========
Name                 Type
==================== ===========
``name``             str
``has_skin``         bool
``skin``             str or None
``trophies``         int
``highest_trophies`` int
``power``            int
==================== ===========

Events
~~~~~~

Returns a result of current and upcoming events.

Attributes:

============ ===================
Name         Type
============ ===================
``current``  List[\Event, Event]
``upcoming`` List[\Event, Event]
============ ===================

Event Attributes:

========================= ====
Name                      Type
========================= ====
``slot``                  int
``slot_name``             str
``start_time``            str
``end_time``              str
``start_time_in_seconds`` int
``end_time_in_seconds``   int
``map_name``              str
``map_image_url``         str
``map_id``                int
``game_mode``             str
``free_keys``             int
``has_modifier``          bool
``modifier_name``         str
``modifier_id``           int
========================= ====

Misc Data
~~~~~~~~~

Returns misc data such as shop and season info.

Attributes:

===================================== ====
Name                                  Type
===================================== ====
``time_until_season_end_in_seconds``  int
``time_until_season_end``             str
``time_until_shop_reset_in_seconds``  int
``time_until_shop_reset``             str
``server_date_year``                  int
``server_date_day_of_year``           int
===================================== ====

Battle Logs
~~~~~~~~~~~

Returns a list of objects with this structure:

Attributes:

::

    {
        "battleTime":"20190706T151526.000Z",
        "event":{
            "id":15000126,
            "mode":"duoShowdown",
            "map":"Royal Runway"
        },
        "battle":{
            "mode":"duoShowdown",
            "type":"ranked",
            "rank":1,
            "trophyChange":9,
            "teams":[
                [
                    {
                        "tag":"#Y2QPGG",
                        "name":"Lex_YouTube",
                        "brawler":{
                            "id":16000005,
                            "name":"SPIKE",
                            "power":10,
                            "trophies":495
                        }
                    },
                    {
                        "tag":"#8Q229LJY",
                        "name":"Brandon",
                        "brawler":{
                            "id":16000003,
                            "name":"BROCK",
                            "power":10,
                            "trophies":495
                        }
                    },
                        {
                        "tag":"#29RGL0QJ0",
                        "name":"smallwhitepeen1",
                        "brawler":{
                            "id":16000007,
                            "name":"JESSIE",
                            "power":7,
                            "trophies":486
                        }
                    }
                ],
                [
                    {
                        "tag":"#CYLVL8LY",
                        "name":"TST|ROYER™",
                        "brawler":{
                            "id":16000019,
                            "name":"PENNY",
                            "power":8,
                            "trophies":541
                        }
                    },
                    {
                        "tag":"#8P2URCR0",
                        "name":"ANOTHER",
                        "brawler":{
                            "id":16000023,
                            "name":"LEON",
                            "power":8,
                            "trophies":559
                        }
                    },
                    {
                        "tag":"#8LRY92QP",
                        "name":"Marshmello",
                        "brawler":{
                            "id":16000021,
                            "name":"GENE",
                            "power":7,
                            "trophies":448
                        }
                    }
                ]
            ]
        }
    }


OfficialAPI
-----------

.. autoclass:: brawlstats.OfficialAPI
    :members:

.. autoclass:: brawlstats.officialapi.core.Client
    :members:

Data Models
~~~~~~~~~~~

.. autoclass:: brawlstats.officialapi.models.Player
    :members:

.. autoclass:: brawlstats.officialapi.models.Club
    :members:

.. autoclass:: brawlstats.officialapi.models.Ranking
    :members:

.. autoclass:: brawlstats.officialapi.models.BattleLog
    :members:

.. autoclass:: brawlstats.officialapi.models.Members
    :members:

.. autoclass:: brawlstats.officialapi.models.Constants
    :members:


Player
~~~~~~

A full player object (all its statistics)


Attributes:

============================ =======================
Name                         Type
============================ =======================
``name``                     str
``name_color``               str
``trophies``                 int
``highest_trophies``         int
``exp_level``                int
``exp_points``               int
``3_vs_3_victories``         int
``solo_victories``           int
``duo_victories``            int
``best_robo_rumble_time``    int
``best_time_as_big_brawler`` int
``club.tag``                 str
``club.name``                str
``brawlers``                 List[\Brawler, Brawler]
============================ =======================

Club
~~~~

A full club object to get a club's statistics. In order to get this, you
must get it from the client or a player object.


Attributes:

===================== =====================
Name                  Type
===================== =====================
``tag``               str
``name``              str
``description``       str
``type``              str
``trophies``          int
``required_trophies`` int
``members``           List[\Member, Member]
===================== =====================

Members
~~~~~~~

Returns a list of club members. Get this by accessing
Club.members or Club.get_members()

.. code:: py

   members = club.members
   print(members[0].name, members[0].role) # prints best player's name and role (sorted by trophies)

Attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``name_color`` str
``role``       str
``trophies``   int
============== ====

Ranking
~~~~~~~

Returns a list of top players, clubs, or brawlers. To access this, do ``ranking[index]``

Player attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``name_color`` str
``trophies``   int
``rank``       int
``club.name``  str
============== ====

Club attributes:

================ ====
Name             Type
================ ====
``tag``          str
``name``         str
``trophies``     int
``rank``         int
``member_count`` int
================ ====

Brawler attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``name_color`` str
``trophies``   int
``rank``       int
``club.name``  str
============== ====

Brawler
~~~~~~~

Returns a brawler object with the following attributes. You can retrieve
a profile’s brawler info by getting Profile.brawlers

.. code:: py

   brawlers = profile.brawlers
   top_brawler = brawlers[0] # first index in list = highest trophies
   print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

Attributes:

==================== ==============
Name                 Type
==================== ==============
``id``               int
``name``             str
``power``            int
``rank``             int
``trophies``         int
``highest_trophies`` int
``star_powers``      List\[SP, SP\]
==================== ==============

Star Power
~~~~~~~~~~

Attributes:

======== ====
Name     Type
======== ====
``id``   int
``name`` str
======== ====

Battle Logs
~~~~~~~~~~~

Returns a list of objects with this structure:

Attributes:

::

    {
        "battleTime":"20190706T151526.000Z",
        "event":{
            "id":15000126,
            "mode":"duoShowdown",
            "map":"Royal Runway"
        },
        "battle":{
            "mode":"duoShowdown",
            "type":"ranked",
            "rank":1,
            "trophyChange":9,
            "teams":[
                [
                    {
                        "tag":"#Y2QPGG",
                        "name":"Lex_YouTube",
                        "brawler":{
                            "id":16000005,
                            "name":"SPIKE",
                            "power":10,
                            "trophies":495
                        }
                    },
                    {
                        "tag":"#8Q229LJY",
                        "name":"Brandon",
                        "brawler":{
                            "id":16000003,
                            "name":"BROCK",
                            "power":10,
                            "trophies":495
                        }
                    },
                        {
                        "tag":"#29RGL0QJ0",
                        "name":"smallwhitepeen1",
                        "brawler":{
                            "id":16000007,
                            "name":"JESSIE",
                            "power":7,
                            "trophies":486
                        }
                    }
                ],
                [
                    {
                        "tag":"#CYLVL8LY",
                        "name":"TST|ROYER™",
                        "brawler":{
                            "id":16000019,
                            "name":"PENNY",
                            "power":8,
                            "trophies":541
                        }
                    },
                    {
                        "tag":"#8P2URCR0",
                        "name":"ANOTHER",
                        "brawler":{
                            "id":16000023,
                            "name":"LEON",
                            "power":8,
                            "trophies":559
                        }
                    },
                    {
                        "tag":"#8LRY92QP",
                        "name":"Marshmello",
                        "brawler":{
                            "id":16000021,
                            "name":"GENE",
                            "power":7,
                            "trophies":448
                        }
                    }
                ]
            ]
        }
    }
