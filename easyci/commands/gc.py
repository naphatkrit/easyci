import click

from easyci import locking
from easyci.history import get_committed_signatures, get_staged_signatures
from easyci.results import get_signatures_with_results, remove_results
from easyci.utils import decorators


@click.command('gc')
@click.pass_context
@decorators.print_markers
def gc(ctx):
    """Runs housekeeping tasks to free up space.

    For now, this only removes saved but unused (unreachable) test results.
    """
    vcs = ctx.obj['vcs']
    count = 0
    with locking.lock(vcs, locking.Lock.tests_history):
        known_signatures = set(get_committed_signatures(vcs) + get_staged_signatures(vcs))
        for signature in get_signatures_with_results(vcs):
            if signature not in known_signatures:
                count += 1
                remove_results(vcs, signature)
    click.echo('Removed {} saved results.'.format(count))
