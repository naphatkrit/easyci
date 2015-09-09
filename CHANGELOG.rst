Change Logs
-----------
2.0.1
=====
- print markers around command output to separate EasyCI outputs from other outputs
- fixed a typo in one of the outputs

2.0.0
=====
- automatically run tests on any changes with :code:`eci watch`.
- :code:`eci test` now deals with concurrency properly.
- test results are now saved for previous test runs and copied over when running :code:`eci test`.
- added a change logs file.

1.6.2
=====
- fixed a bug with :code:`eci test` when running on :code:`pre-push` hooks for certain versions of git.

1.6.1
=====
- updated README.

1.6.0
=====
- clear test history with :code:`eci clear-history`.
- :code:`eci test` now more descriptive of what it is doing.
- updated documentations.

1.5.0
=====
- collect test results by using the config key :code:`collect_results`.

1.4.0
=====
- switched to :code:`rsync` to improve the performance of :code:`eci test`.

1.3.0
=====
- keeping track of which version of EasyCI is installed in a project.
- stops stamping commit messages - this turns out to be tricky.
- various bug fixes.

1.2.1
=====
- added keywords for PyPI.

1.2.0
=====
- updated git hooks to print out more meaningful messages.

1.1.0
=====
- stamp commit messages with EasyCI to indicate that tests were run.

1.0.1
=====
- updated README.

1.0.0
=====
Initial release.
