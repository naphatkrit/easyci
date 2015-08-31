import click

import easyci

from easyci.commands.clear_history import clear_history
from easyci.commands.init import init
from easyci.commands.test import test
from easyci.vcs.git import GitVcs
from easyci.version import get_installed_version, VersionNotInstalledError


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=easyci.__version__, prog_name='EasyCI')
@click.pass_context
def cli(ctx):
    git = GitVcs()
    if ctx.args[0] != 'init':
        try:
            version = get_installed_version(git)
        except VersionNotInstalledError:
            click.echo('Please run `eci init` first.')
            ctx.abort()
        if version != easyci.__version__:
            click.echo('EasyCI version mismatch. Please rerun `eci init`.')
            ctx.abort()

cli.add_command(clear_history)
cli.add_command(init)
cli.add_command(test)
