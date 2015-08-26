import click

from easyci.commands.test import test

@click.group()
def cli():
    pass

cli.add_command(test)
