"""
This module is inspired by the open-sourced project Changes:
https://github.com/dropbox/changes
"""
from __future__ import absolute_import

import os
import os.path

from subprocess import Popen, PIPE


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

        This is available as a class method as it is usually needed to
        initialize the VCS object itself.

        Args:
            cls (class object): The class

        Returns:
            str - the path to the working directory

        Raises:
            CommandError
        """
        raise NotImplementedError
