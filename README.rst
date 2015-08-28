EasyCI
======

**Note**: EasyCI only works with git repositories.

CI for mortals. Never worry about checking in broken code again. No need to maintain a CI server. No need to shell out ridiculous amount of money for your personal project. EasyCI puts your mind at ease, like a good CI service, but without all the extra costs.

EasyCI operates via git :code:`pre-commit` and :code:`pre-push` hooks to ensure that your code passes tests before letting you commit/push.

.. code-block:: bash

    $ git commit
    Running test: flake8
    Passed
    [master b2e6fa1] test commit
    1 file changed, 2 insertions(+), 2 deletions(-)

EasyCI also makes sure not to run tests redundantly. If you ran tests before using :code:`eci test`, and no files have changed, then it does not try to run tests again.

.. code-block:: bash

    $ eci test
    Running test: flake8
    Passed
    $ git commit
    OK Files not changed
    [master b2e6fa1] test commit
    1 file changed, 2 insertions(+), 2 deletions(-)

This means that if you run tests regularly as part of your workflow, there is effectively no efficiency cost in using EasyCI, yet you can rest easy knowing that if you forgot to run tests, you will not be allowed to commit/push.

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
