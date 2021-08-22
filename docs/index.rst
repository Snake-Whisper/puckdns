.. puckdns documentation master file, created by
   sphinx-quickstart on Sun Jul 18 11:25:14 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Puckdns documentation
=====================

|codecov| |githubCI|

.. |codecov| image:: https://codecov.io/gh/Snake-Whisper/puckdns/branch/master/graph/badge.svg?token=7R83F1FHXO
   :target: https://codecov.io/gh/Snake-Whisper/puckdns

.. |githubCI| image:: https://github.com/Snake-Whisper/puckdns/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/Snake-Whisper/puckdns


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents:

   index

This API provides access functionality to the `free secondary puck DNS <https://puck.nether.net/dns/>`_ service.


Installation or upgrade
-----------------------

.. code-block:: bash

   pip3 install -U puckdns

Get started
-----------

.. code-block:: python

   import puckdns
   from puckdns import puckdnsExceptions

   # initialise puck dns class
   puck = puckdns.API()

   # login with your credentials
   try:
      puck.login ("<myusername>", "<mypassword>")
   except puckdnsExceptions.LoginFailed:
      print ("[FATAL] Login failed. False login credentials.")
   else:
      # do something with the API, eg.
      registered_domains = puck.getDomains()
   finally:
      # close connection clean
      puck.logout()

API Reference
-------------
.. automodule:: puckdns
   :members:

Indices and tables
------------------
      
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`