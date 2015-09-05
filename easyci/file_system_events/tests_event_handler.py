import click
import os
import subprocess32 as subprocess
import watchdog.events
import watchdog.utils

from multiprocessing import dummy as multiprocessing

from easyci.file_system_events.vcs_event_handler import VcsEventHandler


class TestsEventHandler(VcsEventHandler):

    def __init__(self, vcs):
        super(TestsEventHandler, self).__init__(vcs)
        self.pool = multiprocessing.Pool()

    def _get_relative_path(self, path):
        return os.path.relpath(path, self.vcs.path)

    def _get_event_string(self, event):
        src = self._get_relative_path(
            watchdog.utils.unicode_paths.decode(event.src_path))
        if event.event_type == watchdog.events.EVENT_TYPE_CREATED:
            return 'Created: ' + src
        elif event.event_type == watchdog.events.EVENT_TYPE_DELETED:
            return 'Deleted: ' + src
        elif event.event_type == watchdog.events.EVENT_TYPE_MODIFIED:
            return 'Modified: ' + src
        elif event.event_type == watchdog.events.EVENT_TYPE_MOVED:
            dest = self._get_relative_path(
                watchdog.utils.unicode_paths.decode(event.dest_path))
            return 'Moved: {src} to {dest}'.format(src=src, dest=dest)
        else:
            return str(event)

    def on_any_event(self, event):
        str_event = self._get_event_string(event)

        def callback(code):
            if code == 0:
                status = click.style('Passed', bg='green', fg='black')
            else:
                status = click.style('Failed', bg='red', fg='black')
            click.echo(status + ' ' + str_event)
        click.echo(click.style('Detected', bg='yellow',
                               fg='black') + ' ' + str_event)
        devnull = open(os.devnull, 'w')
        self.pool.apply_async(subprocess.call, [['eci', 'test']], {
            'stdout': devnull,
            'stderr': devnull,
        }, callback=callback)
