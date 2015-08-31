import mock
import os
import pytest

from easyci.history import (
    add_signature, clear_history, get_known_signatures, _get_history_path
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


@pytest.fixture(scope='function')
def fake_user_config():
    return {
        'history_limit': 5,
    }


def test_get_known_signatures(fake_vcs):
    assert get_known_signatures(fake_vcs) == []

    signatures = ['signature1', 'signature2', 'signature3']
    with open(_get_history_path(fake_vcs), 'w') as f:
        f.write('\n'.join(signatures))

    assert get_known_signatures(fake_vcs) == signatures


def test_add_signature(fake_vcs, fake_user_config):
    history_path = _get_history_path(fake_vcs)

    add_signature(fake_vcs, fake_user_config, 'signature1')
    with open(history_path, 'r') as f:
        assert f.read().strip().split() == ['signature1']

    signatures = ['signature' + str(i) for i in range(fake_user_config['history_limit'])]

    for s in signatures:
        add_signature(fake_vcs, fake_user_config, s)

    with open(history_path, 'r') as f:
        assert f.read().strip().split() == signatures


def test_clear_history(fake_vcs):
    history_path = _get_history_path(fake_vcs)
    assert not os.path.exists(history_path)
    clear_history(fake_vcs)  # when file does not exist
    assert not os.path.exists(history_path)

    with open(history_path, 'w') as f:
        f.write('test')
    assert os.path.exists(history_path)

    clear_history(fake_vcs)
    assert not os.path.exists(history_path)
