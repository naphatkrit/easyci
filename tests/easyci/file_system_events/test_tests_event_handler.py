import mock
import os
import pytest

from watchdog import events

from easyci.file_system_events.tests_event_handler import TestsEventHandler
from easyci.utils import contextmanagers
from easyci.vcs.base import Vcs


@pytest.yield_fixture(scope='function')
def repo_path():
    with contextmanagers.temp_dir() as temp_dir:
        os.mkdir(os.path.join(temp_dir, '.git'))
        yield temp_dir


@pytest.fixture(scope='function')
def fake_vcs(repo_path):
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
    vcs.repository_dir.return_value = os.path.join(repo_path, '.git')
    vcs.get_ignored_files.return_value = [os.path.join(repo_path, 'a/1.txt'),
                                          os.path.join(repo_path, 'a/2.txt')]
    return vcs


@pytest.fixture(scope='function')
def fake_pool():
    fake = mock.MagicMock()
    return fake


@pytest.fixture(scope='function')
def handler(fake_vcs, fake_pool):
    with mock.patch('easyci.file_system_events.tests_event_handler.multiprocessing.Pool', new=lambda: fake_pool):
        handler = TestsEventHandler(fake_vcs)
    return handler


def test_simple(repo_path, handler, fake_pool):
    handler.dispatch(events.FileMovedEvent(os.path.join(
        repo_path, 'test'), os.path.join(repo_path, 'test2')))
    assert fake_pool.apply_async.call_count == 1
