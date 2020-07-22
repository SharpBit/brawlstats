API Reference
=============

.. autoclass:: brawlstats.Client
    :members:

Data Models
~~~~~~~~~~~

.. autoclass:: brawlstats.models.Player
    :members:

.. autoclass:: brawlstats.models.Club
    :members:

.. autoclass:: brawlstats.models.Ranking
    :members:

.. autoclass:: brawlstats.models.BattleLog
    :members:

.. autoclass:: brawlstats.models.Members
    :members:

.. autoclass:: brawlstats.models.Constants
    :members:

.. autoclass:: brawlstats.models.Brawlers
    :members:


Attributes of Data Models
~~~~~~~~~~~~~~~~~~~~~~~~~

Note: These are subject to change at any time. Visit https://developer.brawlstars.com/#/documentation to view up-to-date information on the API.

Player
~~~~~~

A full player object (all its statistics)


Attributes:

============================================ =============
Name                                         Type
============================================ =============
``tag``                                      str
``name``                                     str
``name_color``                               str
``trophies``                                 int
``highest_trophies``                         int
``power_play_points``                        int
``highest_power_play_points``                int
``exp_level``                                int
``exp_points``                               int
``is_qualified_from_championship_challenge`` bool
``x3vs3_victories``                          int
``team_victories``                           int
``solo_victories``                           int
``duo_victories``                            int
``best_robo_rumble_time``                    int
``best_time_as_big_brawler``                 int
``club.tag``                                 str
``club.name``                                str
``brawlers``                                 List[Brawler]
============================================ =============

Club
~~~~

A full club object to get a club's statistics. In order to get this, you
must get it from the client or a player object.


Attributes:

===================== ============
Name                  Type
===================== ============
``tag``               str
``name``              str
``description``       str
``type``              str
``trophies``          int
``required_trophies`` int
``members``           List[Member]
===================== ============

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

Player/Brawler attributes:

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

Brawler
~~~~~~~

Returns a brawler object with the following attributes. You can retrieve
a profile’s brawler info by getting ``Profile.brawlers``

.. code:: py

   brawlers = profile.brawlers
   top_brawler = brawlers[0] # first index in list = highest trophies
   print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

Attributes:

==================== ========
Name                 Type
==================== ========
``id``               int
``name``             str
``power``            int
``rank``             int
``trophies``         int
``highest_trophies`` int
``star_powers``      List[SP]
==================== ========

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

Brawlers
~~~~~~~~

Returns list of available brawlers and information about them with this structure:

Attributes:

::

[
    Brawler
]