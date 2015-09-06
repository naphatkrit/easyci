import filelock
import os

from filelock import Timeout

from contextlib import contextmanager
from enum import Enum, unique


# Timeout is imported so it can be imported by other modules as a member
# of this module, not filelock
Timeout


@unique
class Lock(Enum):
    tests_history = 1


def _get_lock_path(vcs, lock_object):
    return os.path.join(vcs.private_dir(), 'locks', lock_object.name)


def init(vcs):
    """Initialize the locking module for a repository
    """
    path = os.path.join(vcs.private_dir(), 'locks')
    if not os.path.exists(path):
        os.mkdir(path)


@contextmanager
def lock(vcs, lock_object, wait=True):
    """A context manager that grabs the lock and releases it when done.

    This blocks until the lock can be acquired.

    Args:
        vcs (easyci.vcs.base.Vcs)
        lock_object (Lock)
        wait (boolean) - whether to wait for the lock or error out

    Raises:
        Timeout
    """
    if wait:
        timeout = -1
    else:
        timeout = 0
    lock_path = _get_lock_path(vcs, lock_object)
    lock = filelock.FileLock(lock_path)
    with lock.acquire(timeout=timeout):
        yield
