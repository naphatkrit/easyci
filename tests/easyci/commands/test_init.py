import mock
import os
import pytest
import yaml

from easyci import exit_codes
from easyci.hooks import hooks_manager
from easyci.vcs.base import Vcs
from easyci.cli import cli


@pytest.fixture(scope='function')
def fake_vcs(runner):
    repo_path = os.getcwd()
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
    vcs.private_dir.return_value = os.path.join(repo_path, '.git/eci')
    return vcs


def test_init_simple(fake_vcs, runner, fake_hooks):
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['init'])
    assert result.exit_code == exit_codes.SUCCESS
    args = fake_vcs.install_hook.call_args_list
    calls = set()
    for pair in args:
        arg, _ = pair  # only get positional arguments
        calls.add(arg)
    for hook in ['pre-push', 'pre-commit']:
        assert (hook, hooks_manager.get_hook(hook)) in calls


def test_init_stale_hooks(fake_vcs, runner, fake_hooks):
    stale_hook_path = os.path.join(fake_vcs.path, '.git/hooks/commit-msg')
    assert not os.system('touch {}'.format(stale_hook_path))
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['init'])
    assert result.exit_code == exit_codes.SUCCESS
    assert not os.path.exists(stale_hook_path)


def test_init_no_config(fake_vcs, runner, fake_hooks):
    config_path = os.path.join(fake_vcs.path, 'eci.yaml')
    os.remove(config_path)
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['init'])
    assert result.exit_code == exit_codes.SUCCESS
    assert os.path.exists(config_path)
    with open(config_path, 'r') as f:
        yaml.safe_load(f.read())
