EasyCI
======

**Note**: This is under development and not ready for prime time.

CI for mortals. The idea is that for every commit, we want to ensure that there is evidence of passing tests.

**Note**: EasyCI only works with git repositories.

Installation/Setup
------------------
First, install EasyCI using :code:`pip`.

.. code-block:: bash

   pip install easyci

Next, setup EasyCI for your project.

.. code-block:: bash

   cd /path/to/project
   eci init

This will install the necessary git hooks and put a trivial config file :code:`eci.yaml`. You should modify the config file to actually run your tests.

Config
------
The config lives in a file at the root of the repository, :code:`eci.yaml`.

========================= ==================== ===========
key                       type                 Description
========================= ==================== ===========
:code:`tests`             :code:`List[string]` This is a list of commands to run tests.
:code:`history_limit`     :code:`int`          The number of passing test runs to remember.
========================= ==================== ===========

Commands
--------
eci init
+++++++++++++
This command is to be run inside the target repository. This installs the necessary hooks (pre-push + pre-commit) to check if tests have been run for the current commit.


eci test
++++++++
This command creates a copy of your project and remove any ignored files before running tests. If tests pass, then it stores a hash representing the current state of your project in :code:`.git/eci/passed`.
