import click
import os
import subprocess32 as subprocess

from easyci.history import get_known_signatures, add_signature
from easyci.utils import contextmanagers
from easyci.user_config import (
    load_user_config, ConfigFormatError, ConfigNotFoundError,
    _default_config
)
from easyci.vcs.git import GitVcs


@click.command()
@click.option('--staged-only', '-s', is_flag=True, default=False, help='Test against staged version of the repo. Remove all unstaged and ignored files before running.')
@click.option('--head-only', '-h', is_flag=True, default=False, help='Test against the current HEAD. Resets to HEAD and remove all ignored files before running.')
@click.pass_context
def test(ctx, staged_only, head_only):
    """Run tests. If a passing test run is found in the tests run history,
    then this does not run any tests.
    """
    git = GitVcs()

    click.echo('Making a temporary copy of your project...', nl=False)
    with git.temp_copy() as copy:
        click.echo('Done.')
        if head_only:
            click.echo('Resetting to HEAD...', nl=False)
            copy.clear('HEAD')
            click.echo('Done.')
        elif staged_only:
            click.echo('Resetting to staged files...', nl=False)
            copy.remove_unstaged_files()
            click.echo('Done.')

        click.echo('Loading config file...', nl=False)
        try:
            config = load_user_config(copy)
            click.echo('Done.')
        except ConfigFormatError:
            click.echo("Invalid config")
            ctx.abort()
        except ConfigNotFoundError:
            click.echo("No config file")
            config = _default_config

        click.echo('Checking if tests were already ran...', nl=False)
        known_signatures = get_known_signatures(copy)
        new_signature = copy.get_signature()
        if new_signature in known_signatures:
            click.echo('')
            click.echo(click.style('OK', bg='green', fg='black') +
                       ' Tests already ran.')
            ctx.exit(0)
        click.echo('Done.')
        with contextmanagers.chdir(copy.path):
            all_passed = True
            for test in config['tests']:
                click.echo('Running test: {}'.format(test))

                # ok to use shell=True, as the whole point of EasyCI is to run
                # arbitrary code
                ret = subprocess.call(test, shell=True)
                if ret == 0:
                    click.secho('Passed', bg='green', fg='black')
                else:
                    click.secho('Failed', bg='red', fg='black')
                    all_passed = False

        # collect results
        if len(config['collect_results']) > 0:
            click.echo('Collecting test results...', nl=False)
            includes = ['--include={}'.format(x)
                        for x in config['collect_results']]
            cmd = ['rsync', '-r'] + includes + ['--exclude=*',
                                                os.path.join(copy.path, ''), os.path.join(git.path, '')]
            subprocess.check_call(cmd)
            click.echo('Done.')

        if not all_passed:
            ctx.exit(1)
        else:
            add_signature(git, config, new_signature)
