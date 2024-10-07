Setting Up Logging
==================

*brawlstats* logs errors and debug information via the :mod:`logging` python
module. It is strongly recommended that the logging module is
configured, as no errors or warnings will be output if it is not set up.
Configuration of the ``logging`` module can be as simple as

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)

Placed at the start of the application. This will output the logs from
*brawlstats* as well as other libraries that uses the ``logging`` module
directly to the console.

The optional ``level`` argument specifies what level of events to log
out and can any of ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, and
``DEBUG`` and if not specified defaults to ``WARNING``.

More advanced setups are possible with the :mod:`logging` module. For example,
to write the logs to a file called ``brawlstars.log`` instead of
outputting them to to the console, the following snippet can be used:

.. code-block:: python

    import brawlstats
    import logging

    logger = logging.getLogger('brawlstats')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='brawlstars.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

This is recommended, especially at verbose levels such as ``INFO``,
and ``DEBUG`` as there are a lot of events logged and it would clog the
stdout of your program.


Currently, the following things are logged:

- ``DEBUG``: API Requests, Cache Hits



For more information, check the documentation and tutorial of the
:mod:`logging` module.