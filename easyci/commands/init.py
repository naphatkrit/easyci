import click
import os
import yaml

from easyci.hooks import hooks_manager
from easyci.vcs.git import GitVcs


@click.command()
def init():
    git = GitVcs()
    click.echo("Installing hooks")
    git.install_hook('pre-commit', hooks_manager.get_hook('pre-commit'))
    git.install_hook('pre-push', hooks_manager.get_hook('pre-push'))
    git.install_hook('commit-msg', hooks_manager.get_hook('commit-msg'))

    config_path = os.path.join(git.path, 'eci.yaml')
    if not os.path.exists(config_path):
        click.echo("Placing a trivial config file in your project.")
        with open(config_path, 'w') as f:
            f.write(yaml.safe_dump(
                {'tests': ['echo please modify to run your tests', 'true']}))
