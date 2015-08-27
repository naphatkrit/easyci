import click
import os

from easyci.utils import contextmanagers
from easyci.vcs.git import GitVcs


@click.command()
@click.pass_context
def test(ctx):
    git = GitVcs()
    with git.temp_copy() as copy:
        with contextmanagers.chdir(copy.path):
            copy.remove_ignored_files()
            copy.remove_unstaged_files()
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
