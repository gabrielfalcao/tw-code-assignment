ThoughtWorks Code Assignment
============================

.. note:: All the instructions in the readme assume that you have a
          *bash* console to your avail. It has been tested on `*MacOSX
          Sierra* <https://www.apple.com/macos/sierra/>`_ with
          *`Homebrew<http://brew.sh/>`_ **1.1.9**.*

Features:
---------

- unit test coverage with report
- ``Makefile`` commented line-by-line
- option to run validations in docker :)


Preparing a validation environment
----------------------------------

This project has enabled docker-compose, if you just intend to test
the system this might be an easier way to get it done.

It has been tested with `Docker for Mac
<https://docs.docker.com/docker-for-mac/>`_ version ``1.13.0 (15072)``


Ensure system dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

============== =======
Name           Version
============== =======
Docker         1.13.0
docker compose 1.10.1
============== =======


Run the automated tests
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   docker-compose run tw-code-assigment


Preparing a local development environment
-----------------------------------------

Ensure system dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

============== =======
Name           Version
============== =======
python         2.7.13
virtualenv     15.1.0
GNU Make       3.81
============== =======


Run the automated build install targets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   make setup


Breakdown of installation commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # 1. Create and enter a virtual-env
   virtualenv .venv

   # 2. Enter the virtual-env
   source .venv/bin/activate

   # 3. Upgrade pip
   pip install -U pip

   # 4. Install local dependencies
   pip install -r development.txt


Run the automated tests
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   make
