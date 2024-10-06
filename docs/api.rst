API Reference
=============

Client
~~~~~~

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

============================================ ======================
Name                                         Type
============================================ ======================
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
``x3vs3_victories`` / ``team_victories``     int
``solo_victories``                           int
``duo_victories``                            int
``best_robo_rumble_time``                    int
``best_time_as_big_brawler``                 int
``brawlers``                                 List[`PlayerBrawler`_]
``club.tag``                                 str
``club.name``                                str
``icon.id``                                  int
============================================ ======================

Club
~~~~

A full club object to get a club's statistics. In order to get this, you
must get it from the client or a player object.

Attributes:

===================== ===============
Name                  Type
===================== ===============
``tag``               str
``name``              str
``description``       str
``type``              str
``trophies``          int
``required_trophies`` int
``members``           List[`Member`_]
``badge_id``          int
===================== ===============

Member
~~~~~~

Members is a list of club members. Get this by accessing
``Club.members`` or ``Club.get_members()``.
The club's members are sorted in order of descending trophies.
Each Member in the list has the following attributes:

.. code:: py

   members = club.members
   # Prints club's best player's name and role
   print(members[0].name, members[0].role)

Attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``name_color`` str
``role``       str
``trophies``   int
``icon.id``    int
============== ====

Ranking
~~~~~~~

A list of top players, clubs, or brawlers.
Each item in the list has the following attributes:

Player/Brawler Ranking attributes:

============== ====
Name           Type
============== ====
``tag``        str
``name``       str
``name_color`` str
``trophies``   int
``rank``       int
``club.name``  str
``icon.id``    int
============== ====

Club Ranking attributes:

================ ====
Name             Type
================ ====
``tag``          str
``name``         str
``trophies``     int
``rank``         int
``member_count`` int
``badge_id``     int
================ ====

PlayerBrawler
~~~~~~~~~~~~~

PlayerBrawlers is a list of brawler objects, each with the following attributes.
The brawlers are sorted in order of descending trophies.
Note: ``PlayerBrawler`` only represents a brawler that a player owns and 
can only be accessed from ``Player.brawlers``.

.. code:: py

   brawlers = player.brawlers
   # List is sorted by descending trophies
   top_brawler = brawlers[0]
   # print the player's best brawler's name and trophies
   print(top_brawler.name, top_brawler.trophies)

Attributes:

==================== ==================
Name                 Type
==================== ==================
``id``               int
``name``             str
``power``            int
``rank``             int
``trophies``         int
``highest_trophies`` int
``star_powers``      List[`StarPower`_]
``gadgets``          List[`Gadget`_]
``gears``            List[`Gear`_]
==================== ==================

StarPower
~~~~~~~~~

Attributes:

======== ====
Name     Type
======== ====
``id``   int
``name`` str
======== ====

Gadget
~~~~~~

Attributes:

======== ====
Name     Type
======== ====
``id``   int
``name`` str
======== ====

Gear
~~~~

Attributes:

========= ====
Name      Type
========= ====
``id``    int
``name``  str
``level`` int
========= ====

BattleLog
~~~~~~~~~

A BattleLog contains a list of items, each with the following attributes:

Attributes:

=============== ===============
Name            Type
=============== ===============
``battle_time`` str
``event``       `Event`_
``battle``      List[`Battle`_]
=============== ===============

Event
~~~~~

An object containing information about an event.

Attributes:

======== ====
Name     Type
======== ====
``id``   int
``mode`` str
``map``  str
======== ====

Battle
~~~~~~

Each Battle object contains information about a battle.
Note: The ``star_player`` attribute may not exist for certain modes
that do not have a star player (e.g. showdown, duoShowdown).

Attributes:

==================== ===========================
Name                 Type
==================== ===========================
``mode``             str
``type``             str
``result``           str
``duration``         int
``trophy_change``    int
``star_player``      `BattlePlayer`_
``teams``            List[List[`BattlePlayer`_]]
==================== ===========================

BattlePlayer
~~~~~~~~~~~~

Represents a player who played in a battle.

=========== ================
Name        Type
=========== ================
``tag``     str
``name``    str
``brawler`` `BattleBrawler`_
=========== ================

BattleBrawler
~~~~~~~~~~~~~

Represents a brawler that was played in a battle.
Note: ``BattlerBrawler`` only reprents brawlers that were played in a battle
and can only be accessed from ``BattlePlayer.brawler``.

============ ====
Name         Type
============ ====
``id``       int
``name``     str
``power``    int
``trophies`` int
============ ====

Brawlers
~~~~~~~~

Returns list of all brawlers in the game and information,
with each item having the following attributes.
Note: ``Brawlers`` only represents the brawler objects returned
from ``Client.get_brawlers()``.

Attributes:

==================== ==================
Name                 Type
==================== ==================
``id``               int
``name``             str
``star_powers``      List[`StarPower`_]
``gadgets``          List[`Gadget`_]
==================== ==================
