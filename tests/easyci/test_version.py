import mock
import os
import pytest

from easyci.version import (
    get_installed_version, set_installed_version, VersionNotInstalledError,
    _get_version_path,
)
from easyci.utils import contextmanagers
from easyci.vcs.base import Vcs


@pytest.yield_fixture(scope='function')
def temp_path():
    with contextmanagers.temp_dir() as temp_dir:
        yield temp_dir


@pytest.fixture(scope='function')
def fake_vcs(temp_path):
    private_path = os.path.join(temp_path, 'private')
    os.mkdir(private_path)

    vcs = mock.Mock(spec=Vcs)
    vcs.private_dir.return_value = private_path
    return vcs


def test_get_installed_version(fake_vcs):
    with pytest.raises(VersionNotInstalledError):
        get_installed_version(fake_vcs)

    version_path = _get_version_path(fake_vcs)
    with open(version_path, 'w') as f:
        f.write('testing')
    assert get_installed_version(fake_vcs) == 'testing'


def test_set_installed_version(fake_vcs):
    set_installed_version(fake_vcs, 'testing')
    version_path = _get_version_path(fake_vcs)
    with open(version_path, 'r') as f:
        assert f.read() == 'testing'
