import mock
import os
import pytest

from easyci.hooks.hooks_manager import get_hook
from easyci.vcs.base import Vcs
from easyci.cli import cli


@pytest.fixture(scope='function')
def fake_vcs(runner):
    repo_path = os.getcwd()
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
    vcs.private_dir.return_value = os.path.join(repo_path, '.git/eci')
    return vcs


def test_init(fake_vcs, runner):
    with mock.patch('easyci.commands.init.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['init'])
    assert result.exit_code == 0
    args = fake_vcs.install_hook.call_args_list
    calls = set()
    for pair in args:
        arg, _ = pair  # only get positional arguments
        calls.add(arg)
    for hook in ['pre-push', 'pre-commit', 'commit-msg']:
        assert (hook, get_hook(hook)) in calls
