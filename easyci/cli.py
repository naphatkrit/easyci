import click

import easyci

from easyci.commands.init import init
from easyci.commands.test import test
from easyci.user_config import (
    load_user_config, ConfigFormatError, ConfigNotFoundError,
    _default_config
)
from easyci.vcs.git import GitVcs
from easyci.version import get_installed_version, VersionNotInstalledError


@click.group()
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
    try:
        config = load_user_config(git)
    except ConfigFormatError:
        click.echo("Invalid config")
        ctx.abort()
    except ConfigNotFoundError:
        click.echo("No config file")
        config = _default_config
    ctx.obj = dict()
    ctx.obj['config'] = config

cli.add_command(init)
cli.add_command(test)
