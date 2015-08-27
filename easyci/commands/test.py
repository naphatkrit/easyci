import click
import os

from easyci.utils import contextmanagers
from easyci.vcs.git import GitVcs


@click.command()
@click.option('--staged-only', '-s', is_flag=True, default=False, help='Test against staged version of the repo.')
@click.pass_context
def test(ctx, staged_only):
    git = GitVcs()
    evidence_path = os.path.join(git.private_dir(), 'passed')
    known_signatures = []
    if os.path.exists(evidence_path):
        with open(evidence_path, 'r') as f:
            known_signatures = f.read().split()
    with git.temp_copy() as copy:
        copy.remove_ignored_files()
        if staged_only:
            copy.remove_unstaged_files()
        new_signature = copy.get_signature()
        if new_signature in known_signatures:
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
        known_signatures.append(new_signature)
        string = '\n'.join(known_signatures[-ctx.obj['config']['history_limit']:])
        # update evidence file
        with open(evidence_path, 'w') as f:
            f.write(string)
