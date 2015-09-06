import mock
import os
import pytest

from easyci import locking
from easyci.cli import cli
from easyci.vcs.base import Vcs


@pytest.fixture(scope='function')
def fake_vcs(runner):
    vcs = mock.Mock(spec=Vcs)
    vcs.path = os.getcwd()
    vcs.private_dir.return_value = os.path.join(vcs.path, '.git/eci')
    return vcs


@pytest.fixture(scope='function', autouse=True)
def init(runner, fake_vcs):
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        runner.invoke(cli, ['init'])


def test_simple(fake_vcs):
    with locking.lock(fake_vcs, locking.Lock.tests_history):
        pass
