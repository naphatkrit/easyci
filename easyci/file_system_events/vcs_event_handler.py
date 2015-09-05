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
                 if not p.startswith(os.path.realpath(self.vcs.repository_dir()))]
        ignored_paths = set(
            os.path.realpath(os.path.join(self.vcs.path, p))
            for p in self.vcs.get_ignored_files()
        )

        if any(p not in ignored_paths for p in paths):
            super(VcsEventHandler, self).dispatch(event)
