import click

from watchdog.observers import Observer

from easyci.file_system_events.tests_event_handler import TestsEventHandler
from easyci.utils import decorators


@click.command()
@click.pass_context
@decorators.print_markers
def watch(ctx):
    """Watch the directory for changes. Automatically run tests.
    """
    vcs = ctx.obj['vcs']

    event_handler = TestsEventHandler(vcs)

    observer = Observer()
    observer.schedule(event_handler, vcs.path, recursive=True)
    observer.start()
    click.echo('Watching directory `{path}`. Use ctrl-c to stop.'.format(path=vcs.path))
    while observer.isAlive():
        observer.join(timeout=1)
