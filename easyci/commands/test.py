import click
import os

from easyci.utils import contextmanagers
from easyci.vcs.git import GitVcs


@click.command()
@click.pass_context
def test(ctx):
    git = GitVcs()
    evidence_path = os.path.join(git.private_dir(), 'passed')
    old_signature = None
    if os.path.exists(evidence_path):
        with open(evidence_path, 'r') as f:
            old_signature = f.read()
    with git.temp_copy() as copy:
        copy.remove_ignored_files()
        copy.remove_unstaged_files()
        new_signature = copy.get_signature()
        if old_signature == new_signature:
            click.echo(click.style('OK', bg='green', fg='black') + 'Files not changed.')
            ctx.exit(0)
        with contextmanagers.chdir(copy.path):
            all_passed = True
            for test in ctx.obj['config']['tests']:
                click.echo('Running test: {}'.format(test))
                ret = os.system(test)
                if ret == 0:
                    click.secho('Passed', bg='green', fg='black')
                else:
                    click.secho('Failed', bg='red', fg='black')
                    all_passed = False
    if not all_passed:
        ctx.exit(1)
    else:
        # update evidence file
        with open(evidence_path, 'w') as f:
            f.write(new_signature)
