import click
import os


@click.command()
@click.pass_context
def test(ctx):
    for test in ctx.obj['config']['tests']:
        click.echo('Running test: {}'.format(test))
        ret = os.system(test)
        if ret == 0:
            click.secho('Passed', bg='green')
        else:
            click.secho('Failed', bg='red')
