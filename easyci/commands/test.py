import click
import subprocess32 as subprocess

from easyci.history import get_known_signatures, add_signature
from easyci.utils import contextmanagers
from easyci.vcs.git import GitVcs


@click.command()
@click.option('--staged-only', '-s', is_flag=True, default=False, help='Test against staged version of the repo. Remove all unstaged and ignored files before running.')
@click.option('--head-only', '-h', is_flag=True, default=False, help='Test against the current HEAD. Resets to HEAD and remove all ignored files before running.')
@click.pass_context
def test(ctx, staged_only, head_only):
    git = GitVcs()
    known_signatures = get_known_signatures(git)
    with git.temp_copy() as copy:
        copy.remove_ignored_files()
        if head_only:
            copy.clear('HEAD')
        elif staged_only:
            copy.remove_unstaged_files()
        new_signature = copy.get_signature()
        if new_signature in known_signatures:
            click.echo(click.style('OK', bg='green', fg='black') + ' Files not changed.')
            ctx.exit(0)
        with contextmanagers.chdir(copy.path):
            all_passed = True
            for test in ctx.obj['config']['tests']:
                click.echo('Running test: {}'.format(test))

                # ok to use shell=True, as the whole point of EasyCI is to run
                # arbitrary code
                ret = subprocess.call(test, shell=True)
                if ret == 0:
                    click.secho('Passed', bg='green', fg='black')
                else:
                    click.secho('Failed', bg='red', fg='black')
                    all_passed = False
    if not all_passed:
        ctx.exit(1)
    else:
        add_signature(git, ctx.obj['config'], new_signature)
