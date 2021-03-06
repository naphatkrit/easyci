EasyCI
======
**Note**: EasyCI only works with git repositories.

Never worry about checking in broken code again. No need to maintain a CI server. No need to shell out ridiculous amount of money for your personal project. EasyCI puts your mind at ease, like a good CI service, but without all the extra costs.

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

EasyCI is designed to shift the burden of test running away from you. To that end, it is possible to have EasyCI monitor your project for changes and automatically run tests, so that by the time you want to commit your changes, your tests would have already been run. Do this in a separate shell session:

.. code-block:: bash

    $ # from anywhere in your project
    $ eci watch
    Watching directory `/path/to/project`. Use ctrl-c to stop.

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

Running Tests
-------------
Tests are run automatically by git's :code:`pre-commit` and :code:`pre-push` hooks. To trigger tests manually:

.. code-block:: bash

    # from anywhere in your project
    eci test

Collecting Test Results
-----------------------
EasyCI preserves the state of your project by making a copy of your project using :code:`rsync` to a temporary directory. In some cases, you do want the files generated by your tests. For example, if your tests generate code coverage data, or other tests data, you will want the options to copy those files from the temporary directory back to your project directory. This can be done by the config :code:`collect_results`.

As an example, the following config will copy everything under the subdirectory :code:`htmlcov`, which in this case contains the code coverage report.

.. code-block:: yaml

    tests:
        - coverage run -m py.test && coverage html
    collect_results:
        - htmlcov/***

For more information on the pattern format for :code:`collect_results`, see the man page for :code:`rsync`, which is used internally to copy the test results.


Config
------
The config lives in a file at the root of the repository, :code:`eci.yaml`.

========================= ==================== ===========
key                       type                 Description
========================= ==================== ===========
:code:`tests`             :code:`List[string]` This is a list of commands to run tests.
:code:`history_limit`     :code:`int`          The number of passing test runs to remember.
:code:`collect_results`   :code:`List[string]` Copy files matching these patterns back to the project. The patterns must be in an :code:`rsync`-compatible format.
========================= ==================== ===========

Commands
--------
All commands should be run inside the target repository.

eci init
+++++++++++++
Initialize the project for use with EasyCI. This installs the necessary git hooks (pre-commit + pre-push) and add a config file if one does not already exists.


eci test
++++++++
Run tests. If a passing test run is found in the tests run history, then this does not run any tests.


eci watch
+++++++++
Watch the current repository for changes and automatically run tests.


eci gc
++++++
Runs housekeeping tasks to free up space. For now, this only removes saved but unused (unreachable) test results.


eci clear-history
+++++++++++++++++
Clear tests run history. History is normally used to keep track of whether a test has been run for a specific state of the project, to avoid running tests redundantly. This command clears the history, causing the next `eci test` command to always run tests.
