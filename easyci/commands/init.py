import click
import os
import yaml

import easyci

from easyci.hooks import hooks_manager
from easyci.vcs.git import GitVcs
from easyci.version import set_installed_version


@click.command()
def init():
    # install hooks
    git = GitVcs()
    click.echo("Installing hooks")
    for old in ['commit-msg']:
        path = os.path.join(git.path, '.git/hooks', old)
        if os.path.exists(path):
            os.remove(path)
    for new in ['pre-commit', 'pre-push']:
        git.install_hook(new, hooks_manager.get_hook(new))

    # add a config file if one does not exist
    config_path = os.path.join(git.path, 'eci.yaml')
    if not os.path.exists(config_path):
        click.echo("Placing a trivial config file in your project.")
        with open(config_path, 'w') as f:
            f.write(yaml.safe_dump(
                {'tests': ['echo please modify to run your tests', 'true']}))

    # update installed version
    set_installed_version(git, easyci.__version__)
