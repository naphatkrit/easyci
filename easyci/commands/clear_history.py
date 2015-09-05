import click

from easyci.history import clear_history as clear_history_internal


@click.command('clear-history')
@click.pass_context
def clear_history(ctx):
    """Clear tests run history. History is normally used to keep track of
    whether a test has been run for a specific state of the project, to
    avoid running tests redundantly. This command clears the history,
    causing the next `eci test` command to always run tests.
    """
    git = ctx.obj['vcs']
    clear_history_internal(git)
