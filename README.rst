.. image:: https://i.imgur.com/5uUkTrn.png
    :alt: Brawl Stats

Brawl Stats
===========

.. image:: https://img.shields.io/pypi/v/brawlstats.svg
    :target: https://pypi.org/project/brawlstats/
    :alt: PyPi

.. image:: https://travis-ci.com/SharpBit/brawlstats.svg?branch=master
    :target: https://travis-ci.com/SharpBit/brawlstats
    :alt: Travis-CI build

.. image:: https://img.shields.io/pypi/pyversions/brawlstats.svg
    :target: https://pypi.org/project/brawlstats/
    :alt: Supported Versions

.. image:: https://img.shields.io/github/license/SharpBit/brawlstats.svg
    :target: https://github.com/SharpBit/brawlstats/blob/master/LICENSE
    :alt: MIT License

| This library is a sync and async wrapper the unofficial `Brawl Stars API`_.
| To keep up with API changes, discussions, and status, I recommend you join the `discord server`_.

Features
~~~~~~~~

- Covers all of the API endpoints.
- Use the same client for sync and async usage.
- Helper functions to access other game files such as maps and audio files.
- Easy to use with an object oriented design.

Installation
~~~~~~~~~~~~

Install the latest stable build:

::

   pip install brawlstats

Install the development build:

::

   pip install git+https://github.com/SharpBit/brawlstats

Documentation
~~~~~~~~~~~~~

Documentation is being hosted on `Read the Docs`_.

Examples
~~~~~~~~
Examples are in the `examples folder`_.

- ``sync.py`` shows you basic sync usage
- ``async.py`` shows you basic async usage
- ``discord_cog.py`` shows an example Discord Bot cog using `discord.py rewrite`_

Misc
~~~~

| If you are currently using this wrapper, feel free to star this repository :)
| If you come across an issue in the wrapper, please `create an issue`_. Do **not** PM me on Discord for help.
| If you need an API Key, join the API’s `discord server`_.

Contributing
~~~~~~~~~~~~
If you want to contribute, whether it be a bug fix or new feature, make sure to follow the `contributing guidelines`_.

.. _Brawl Stars API: http://brawlapi.cf/api
.. _create an issue: https://github.com/SharpBit/brawlstats/issues
.. _discord server: https://discord.me/BrawlAPI
.. _Read the Docs: https://brawlstats.rtfd.io/
.. _examples folder: https://github.com/SharpBit/brawlstats/tree/master/examples
.. _discord.py rewrite: https://github.com/rapptz/discord.py/tree/rewrite
.. _contributing guidelines: https://github.com/SharpBit/brawlstats/blob/master/CONTRIBUTING.md