import mock
import pytest
import shutil
import tempfile

from easyci.hooks.hooks_manager import get_hook
from easyci.vcs.base import Vcs
from easyci.cli import cli


@pytest.yield_fixture(scope='function')
def repo_path():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


@pytest.fixture(scope='function')
def fake_vcs(repo_path):
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
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
