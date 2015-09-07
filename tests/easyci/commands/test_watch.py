import mock
import os
import pytest

from watchdog.observers import Observer

from easyci import exit_codes
from easyci.vcs.base import Vcs
from easyci.cli import cli


@pytest.fixture(scope='function')
def fake_vcs(runner):
    repo_path = os.getcwd()
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
    vcs.private_dir.return_value = os.path.join(repo_path, '.git/eci')
    return vcs


@pytest.fixture(scope='function', autouse=True)
def init(runner):
    result = runner.invoke(cli, ['init'])
    assert result.exit_code == exit_codes.SUCCESS


@pytest.fixture(scope='function')
def fake_observer():
    fake = mock.Mock(spec=Observer)
    fake.isAlive.side_effect = [True, False]
    return fake


def test_watch(runner, fake_vcs, fake_observer):
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs), mock.patch('easyci.commands.watch.Observer', new=lambda: fake_observer):
        result = runner.invoke(cli, ['watch'])
    assert result.exit_code == exit_codes.SUCCESS
