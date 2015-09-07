import os

from watchdog.events import FileSystemEventHandler
from watchdog.utils import has_attribute
from watchdog.utils import unicode_paths


class VcsEventHandler(FileSystemEventHandler):

    def __init__(self, vcs):
        super(VcsEventHandler, self).__init__()
        self.vcs = vcs

    def dispatch(self, event):
        """Only dispatch if the event does not correspond to an ignored file.
        Args:
            event (watchdog.events.FileSystemEvent)
        """
        if event.is_directory:
            return
        paths = []
        if has_attribute(event, 'dest_path'):
            paths.append(os.path.realpath(
                unicode_paths.decode(event.dest_path)))
        if event.src_path:
            paths.append(os.path.realpath(
                unicode_paths.decode(event.src_path)))
        paths = [p for p in paths
                 if not p.startswith(os.path.realpath(self.vcs.repository_dir()))
                 and not self.vcs.path_is_ignored(p)]

        if len(paths) > 0:
            super(VcsEventHandler, self).dispatch(event)
