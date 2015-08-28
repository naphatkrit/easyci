import click
import os
import yaml

from easyci.vcs.git import GitVcs


@click.command()
def init():
    git = GitVcs()
    click.echo("Installing hooks")
    git.install_hook('pre-commit', '#!/bin/bash\neci test --staged-only\n')
    git.install_hook('pre-push', '#!/bin/bash\neci test --staged-only\n')

    config_path = os.path.join(git.path, 'eci.yaml')
    if not os.path.exists(config_path):
        click.echo("Placing a trivial config file in your project.")
        with open(config_path, 'w') as f:
            f.write(yaml.safe_dump(
                {'tests': ['echo please modify to run your tests', 'true']}))
