import click

from easyci.vcs.git import GitVcs


@click.command()
def init():
    git = GitVcs()
    click.echo("Installing hooks")
    git.install_hook('pre-commit', '#!/bin/bash\neci test\n')
