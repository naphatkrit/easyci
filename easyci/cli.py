import click

from easyci.commands.init import init
from easyci.commands.test import test
from easyci.user_config import (
    load_user_config, ConfigFormatError, ConfigNotFoundError,
    _default_config
)
from easyci.vcs.git import GitVcs


@click.group()
@click.pass_context
def cli(ctx):
    git = GitVcs()
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
