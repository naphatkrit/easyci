import click
import subprocess32 as subprocess

from easyci import exit_codes, locking
from easyci.history import (
    commit_signature, get_committed_signatures, get_staged_signatures,
    stage_signature, unstage_signature,
)
from easyci.results import save_results, sync_results, ResultsNotFoundError
from easyci.utils import contextmanagers, decorators
from easyci.user_config import (
    load_user_config, ConfigFormatError, ConfigNotFoundError,
    _default_config
)


@click.command()
@click.option('--staged-only', '-s', is_flag=True, default=False, help='Test against staged version of the repo. Remove all unstaged and ignored files before running.')
@click.option('--head-only', '-h', is_flag=True, default=False, help='Test against the current HEAD. Resets to HEAD and remove all ignored files before running.')
@click.pass_context
@decorators.print_markers
def test(ctx, staged_only, head_only):
    """Run tests. If a passing test run is found in the tests run history,
    then this does not run any tests.
    """
    git = ctx.obj['vcs']

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

        click.echo('Checking if tests were already run...', nl=False)
        new_signature = copy.get_signature()

        with locking.lock(git, locking.Lock.tests_history):
            in_committed = new_signature in get_committed_signatures(git)
            in_staged = new_signature in get_staged_signatures(git)
            if not in_committed and not in_staged:
                stage_signature(git, new_signature)
            if in_committed:
                click.echo('')
                click.echo(click.style('OK', bg='green', fg='black') +
                           ' Tests already ran.')
                try:
                    click.echo('Syncing test results...', nl=False)
                    sync_results(git, new_signature)
                    click.echo('Done')
                except ResultsNotFoundError:
                    click.echo('No results to sync.')
                ctx.exit(exit_codes.SUCCESS)
            if in_staged:
                click.echo('')
                click.echo(click.style('In Progress', bg='yellow', fg='black') +
                           ' Tests already running.')
                ctx.exit(exit_codes.ALREADY_RUNNING)
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

        with locking.lock(git, locking.Lock.tests_history):
            # collect results
            if len(config['collect_results']) > 0:
                click.echo('Collecting results...', nl=False)
                save_results(git, new_signature, copy.path,
                             config['collect_results'])
                click.echo('Done')
                click.echo('Syncing test results...', nl=False)
                sync_results(git, new_signature)
                click.echo('Done')

            # save signature
            if not all_passed:
                unstage_signature(git, new_signature)
                ctx.exit(exit_codes.FAILURE)
            else:
                commit_signature(git, config, new_signature)
                ctx.exit(exit_codes.SUCCESS)
