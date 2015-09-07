import mock
import os
import pytest

from easyci.history import (
    commit_signature, clear_history,
    stage_signature, unstage_signature,
    _get_committed_history_path, _get_staged_history_path,
    NotStagedError, AlreadyStagedError, AlreadyCommittedError,
    get_committed_signatures, get_staged_signatures,
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


def test_get_committed_signatures(fake_vcs):
    assert get_committed_signatures(fake_vcs) == []

    # test committed
    signatures = ['signature1', 'signature2', 'signature3']
    with open(_get_committed_history_path(fake_vcs), 'w') as f:
        f.write('\n'.join(signatures))

    # order is guaranteed for committed history
    assert get_committed_signatures(fake_vcs) == signatures


def test_get_staged_signatures(fake_vcs):
    assert get_staged_signatures(fake_vcs) == []

    # test committed
    signatures = ['signature1', 'signature2', 'signature3']
    with open(_get_staged_history_path(fake_vcs), 'w') as f:
        f.write('\n'.join(signatures))

    # order is not guaranteed for staged history
    assert set(get_staged_signatures(fake_vcs)) == set(signatures)


def test_commit_signature(fake_vcs, fake_user_config):
    stage_signature(fake_vcs, 'dummy')
    committed_path = _get_committed_history_path(fake_vcs)
    staged_path = _get_staged_history_path(fake_vcs)

    # test unstaged
    with pytest.raises(NotStagedError):
        commit_signature(fake_vcs, fake_user_config, 'signature1')

    # test staged
    stage_signature(fake_vcs, 'signature1')
    commit_signature(fake_vcs, fake_user_config, 'signature1')
    with open(committed_path, 'r') as f:
        assert f.read().strip().split() == ['signature1']
    with open(staged_path, 'r') as f:
        assert f.read().strip().split() == ['dummy']

    # test commit twice
    stage_signature(fake_vcs, 'signature1')
    with pytest.raises(AlreadyCommittedError):
        commit_signature(fake_vcs, fake_user_config, 'signature1')
    unstage_signature(fake_vcs, 'signature1')

    # test limit
    signatures = ['generatedsignature' + str(i)
                  for i in range(fake_user_config['history_limit'])]

    for s in signatures:
        stage_signature(fake_vcs, s)
        commit_signature(fake_vcs, fake_user_config, s)

    with open(committed_path, 'r') as f:
        assert f.read().strip().split() == signatures
    with open(staged_path, 'r') as f:
        assert f.read().strip().split() == ['dummy']


def test_stage_signature(fake_vcs):
    staged_path = _get_staged_history_path(fake_vcs)

    # test simple staging
    stage_signature(fake_vcs, 'signature1')
    with open(staged_path, 'r') as f:
        assert f.read().strip().split() == ['signature1']

    # test double staging
    with pytest.raises(AlreadyStagedError):
        stage_signature(fake_vcs, 'signature1')


def test_unstage_signature(fake_vcs):
    staged_path = _get_staged_history_path(fake_vcs)

    # test empty case
    with pytest.raises(NotStagedError):
        unstage_signature(fake_vcs, 'signature1')

    # test nonempty case
    with open(staged_path, 'w') as f:
        f.write('signature1\n')
    unstage_signature(fake_vcs, 'signature1')
    with open(staged_path, 'r') as f:
        assert f.read().strip().split() == []


def test_clear_history(fake_vcs):
    history_path = _get_committed_history_path(fake_vcs)
    assert not os.path.exists(history_path)
    clear_history(fake_vcs)  # when file does not exist
    assert not os.path.exists(history_path)

    with open(history_path, 'w') as f:
        f.write('test')
    assert os.path.exists(history_path)

    clear_history(fake_vcs)
    assert not os.path.exists(history_path)
