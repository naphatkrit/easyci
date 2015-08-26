EasyCI
======

**Note**: This is under development and not ready for prime time.

CI for mortals. The idea is that for every commit, we want to ensure that there is evidence of passing tests.

Config
------
The config lives in a file at the root of the repository, :code:`eci.yaml`.

============= ==================== ===========
key           type                 Description
============= ==================== ===========
:code:`tests` :code:`List[string]` This is a list of commands to run tests.
============= ==================== ===========

Commands
--------
eci install
+++++++++++++
This command is to be run inside the target repository. This installs the necessary hooks to check if tests have been run for the current commit.

**Note**: It is unclear whether this will be in a pre-commit or pre-push hook.

eci test
++++++++
Run the test commands specificied in the config, and update the evidence file :code:`.git/eci/ran`
