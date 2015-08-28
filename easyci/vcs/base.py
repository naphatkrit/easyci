"""
This module is inspired by the open-sourced project Changes:
https://github.com/dropbox/changes
"""
from __future__ import absolute_import

import os
import os.path
import shutil

from contextlib import contextmanager
from subprocess import Popen, PIPE

from easyci.utils import contextmanagers


class CommandError(Exception):

    def __init__(self, cmd, retcode, stdout, stderr):
        self.cmd = cmd
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr

    def __unicode__(self):
        return '%s returned %d:\nSTDOUT: %r\nSTDERR: %r' % (
            self.cmd, self.retcode, self.stdout, self.stderr)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class Vcs(object):

    def __init__(self, path=None):
        """Initialize a new Vcs object for a repository located at `path`.
        If `path` is `None`, then `get_working_directory` is used to identify
        the path.

        Args:
            path (str) - optional. The path to the repo working directory.
        """
        self.path = None
        if path is None:
            self.path = self.get_working_directory()
        else:
            self.path = path
        assert self.exists()

    def run(self, *args, **kwargs):
        if self.path is not None:
            # only None when called in the __init__ function
            kwargs.setdefault('cwd', self.path)

        env = os.environ.copy()

        for key, value in kwargs.pop('env', {}):
            env[key] = value

        kwargs['env'] = env
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE

        proc = Popen(args, **kwargs)
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            raise CommandError(args[0], proc.returncode, stdout, stderr)
        return stdout

    def exists(self):
        """Check if the working directory exists

        Returns:
            bool - True if the working directory exists
        """
        return os.path.exists(self.path)

    def get_working_directory(self):
        """Get the working directory for this repo.

        Args:
            cls (class object): The class

        Returns:
            str - the path to the working directory

        Raises:
            CommandError
        """
        raise NotImplementedError

    def install_hook(self, hook_name, hook_content):
        """Install the repository hook for this repo.

        Args:
            hook_name (str)
            hook_content (str)
        """
        raise NotImplementedError

    def remove_ignored_files(self):
        """Remove files ignored by the repository
        """
        raise NotImplementedError

    def remove_unstaged_files(self):
        """Remove all unstaged files. This does NOT remove ignored files.

        TODO this may be specific to git?
        """
        raise NotImplementedError

    def clear(self, target_commit):
        """Resets the repository to the target commit, removing any staged,
        unstaged, and untracked files.

        Args:
            target_commit (str): the commit ID
        Raises:
            CommandError - if the commit does not exist
        """
        raise NotImplementedError

    def private_dir():
        """Get the private directory associated with this repo, but untracked
        by the repo.

        Returns:
            str - path
        """
        raise NotImplementedError

    def get_signature(self):
        """Get the signature of the current state of the repository

        Returns:
            str
        """
        raise NotImplementedError

    @contextmanager
    def temp_copy(self):
        """Yields a new Vcs object that represents a temporary, disposable
        copy of the current repository. The copy is deleted at the end
        of the context.

        Yields:
            Vcs
        """
        with contextmanagers.temp_dir() as temp_dir:
            temp_root_path = os.path.join(temp_dir, 'root')
            shutil.copytree(self.path, temp_root_path)
            copy = self.__class__(path=temp_root_path)
            yield copy
