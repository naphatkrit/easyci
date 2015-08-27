import click
import os


@click.command()
@click.pass_context
def test(ctx):
    all_passed = True
    for test in ctx.obj['config']['tests']:
        click.echo('Running test: {}'.format(test))
        ret = os.system(test)
        if ret == 0:
            click.secho('Passed', bg='green')
        else:
            click.secho('Failed', bg='red')
            all_passed = False
    if not all_passed:
        ctx.exit(1)
