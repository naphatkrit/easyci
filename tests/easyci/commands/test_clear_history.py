import mock
import os
import pytest

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
    runner.invoke(cli, ['init'])


def test_clear_history(runner, fake_vcs):
    with mock.patch('easyci.commands.clear_history.GitVcs', new=lambda: fake_vcs):
        with mock.patch('easyci.commands.clear_history.clear_history_internal') as mocked:
            result = runner.invoke(cli, ['clear-history'])
    mocked.assert_called_once_with(fake_vcs)
    assert result.exit_code == 0
