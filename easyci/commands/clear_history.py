import click

from easyci.history import clear_history as clear_history_internal
from easyci.vcs.git import GitVcs


@click.command('clear-history')
def clear_history():
    git = GitVcs()
    clear_history_internal(git)
