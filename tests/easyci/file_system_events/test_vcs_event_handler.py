import mock
import os
import pytest

from watchdog import events

from easyci.file_system_events.vcs_event_handler import VcsEventHandler
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
    vcs.path_is_ignored = lambda path: 'a/1.txt' in path or 'a/2.txt' in path
    return vcs


@pytest.fixture(scope='function')
def fake_handler(fake_vcs):
    handler = VcsEventHandler(fake_vcs)
    handler.on_any_event = mock.MagicMock()
    handler.on_created = mock.MagicMock()
    handler.on_deleted = mock.MagicMock()
    handler.on_modified = mock.MagicMock()
    handler.on_moved = mock.MagicMock()
    return handler


def test_dirs(repo_path, fake_handler):
    fake_handler.dispatch(events.DirMovedEvent(os.path.join(
        repo_path, 'test'), os.path.join(repo_path, 'test2')))
    fake_handler.dispatch(events.DirModifiedEvent(os.path.join(
        repo_path, 'test')))
    fake_handler.dispatch(events.DirCreatedEvent(os.path.join(
        repo_path, 'test')))
    fake_handler.dispatch(events.DirDeletedEvent(os.path.join(
        repo_path, 'test')))
    assert fake_handler.on_any_event.call_count == 0
    assert fake_handler.on_created.call_count == 0
    assert fake_handler.on_deleted.call_count == 0
    assert fake_handler.on_modified.call_count == 0
    assert fake_handler.on_moved.call_count == 0


def test_moved(repo_path, fake_handler):
    fake_handler.dispatch(events.FileMovedEvent(os.path.join(
        repo_path, 'test'), os.path.join(repo_path, 'test2')))
    assert fake_handler.on_any_event.call_count == 1
    assert fake_handler.on_created.call_count == 0
    assert fake_handler.on_deleted.call_count == 0
    assert fake_handler.on_modified.call_count == 0
    assert fake_handler.on_moved.call_count == 1


def test_modified(repo_path, fake_handler):
    fake_handler.dispatch(events.FileModifiedEvent(os.path.join(
        repo_path, 'test')))
    assert fake_handler.on_any_event.call_count == 1
    assert fake_handler.on_created.call_count == 0
    assert fake_handler.on_deleted.call_count == 0
    assert fake_handler.on_modified.call_count == 1
    assert fake_handler.on_moved.call_count == 0


def test_created(repo_path, fake_handler):
    fake_handler.dispatch(events.FileCreatedEvent(os.path.join(
        repo_path, 'test')))
    assert fake_handler.on_any_event.call_count == 1
    assert fake_handler.on_created.call_count == 1
    assert fake_handler.on_deleted.call_count == 0
    assert fake_handler.on_modified.call_count == 0
    assert fake_handler.on_moved.call_count == 0


def test_deleted(repo_path, fake_handler):
    fake_handler.dispatch(events.FileDeletedEvent(os.path.join(
        repo_path, 'test')))
    assert fake_handler.on_any_event.call_count == 1
    assert fake_handler.on_created.call_count == 0
    assert fake_handler.on_deleted.call_count == 1
    assert fake_handler.on_modified.call_count == 0
    assert fake_handler.on_moved.call_count == 0


def test_ignored(repo_path, fake_handler):
    fake_handler.dispatch(events.FileModifiedEvent(os.path.join(
        repo_path, 'a/1.txt')))
    fake_handler.dispatch(events.FileModifiedEvent(os.path.join(
        repo_path, 'a/2.txt')))
    fake_handler.dispatch(events.FileModifiedEvent(os.path.join(
        repo_path, '.git/eci/version')))
    assert fake_handler.on_any_event.call_count == 0
    assert fake_handler.on_created.call_count == 0
    assert fake_handler.on_deleted.call_count == 0
    assert fake_handler.on_modified.call_count == 0
    assert fake_handler.on_moved.call_count == 0
