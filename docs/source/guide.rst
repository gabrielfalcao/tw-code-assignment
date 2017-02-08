Development Guide
=================

.. note:: The instructions below assume that you have a *bash* console
          to your avail. It has been tested on `MacOSX Sierra <https://www.apple.com/macos/sierra/>`_ with
          `Homebrew **1.1.9** <http://brew.sh/>`_

**Features:**

- unit + functional tests with coverage report
- ``Makefile`` targets to automate menial development tasks
- ``Dockerfile`` that builds and tests the project in a sandboxed container
- Auto-generated API documentation

.. _Guide:

Build a docker image
--------------------

.. note:: Tested on `Docker for Mac <https://docs.docker.com/docker-for-mac/>`_ version ``1.13.0 (5072)``

.. code:: bash

   docker build . -t tw-code-assignment
   docker run tw-code-assignment


Preparing a local development environment
-----------------------------------------

**Ensure system dependencies:**

============== =======
**Python**     2.7.13
**virtualenv** 15.1.0
**GNU Make**   3.81
============== =======


**Run the automated build install targets:**

.. code:: bash

   make setup


**Breakdown of installation commands:**

.. code:: bash

   # 1. Create and enter a virtual-env
   virtualenv .venv

   # 2. Enter the virtual-env
   source .venv/bin/activate

   # 3. Upgrade pip
   pip install -U pip

   # 4. Install local dependencies
   pip install -r development.txt


**Run the automated tests:**

.. code:: bash

   make tests


Instalation
-----------

.. code-block:: bash

    python setup.py install


Command-Line Example
--------------------

.. code:: bash

   $ cat test-input.txt <<EOF
   Writing Fast Tests Against Enterprise Rails 60min
   Overdoing it in Python 45min
   Lua for the Masses 30min
   Ruby Errors from Mismatched Gem Versions 45min
   Common Ruby Errors 45min
   Rails for Python Developers lightning
   Communicating Over Distance 60min
   Accounting-Driven Development 45min
   Woah 30min
   Sit Down and Write 30min
   Pair Programming vs Noise 45min
   Rails Magic 60min
   Ruby on Rails: Why We Should Move On 60min
   Clojure Ate Scala (on my project) 45min
   Programming in the Boondocks of Seattle 30min
   Ruby vs. Clojure for Back-End Development 30min
   Ruby on Rails Legacy App Maintenance 60min
   A World Without HackerNews 30min
   User Interface CSS in Rails Apps 30min
   EOF
   $ tw-conf-parse test-input.txt
