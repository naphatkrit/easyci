import click

from easyci.history import clear_history as clear_history_internal
from easyci.vcs.git import GitVcs


@click.command('clear-history')
def clear_history():
    """Clear tests run history. History is normally used to keep track of
    whether a test has been run for a specific state of the project, to
    avoid running tests redundantly. This command clears the history,
    causing the next `eci test` command to always run tests.
    """
    git = GitVcs()
    clear_history_internal(git)
