import mock
import os
import pytest
import shutil
import tempfile

from click.testing import CliRunner

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


def test_init(fake_vcs):
    with mock.patch('easyci.commands.init.GitVcs', new=lambda: fake_vcs):
        runner = CliRunner()
        with runner.isolated_filesystem():
            assert not os.system('git init')
            with mock.patch('easyci.cli.load_user_config') as mocked:
                mocked.return_value = {}
                result = runner.invoke(cli, ['init'])
    assert result.exit_code == 0
    fake_vcs.install_hook.assert_called_once_with(
        'pre-commit', '#!/bin/bash\neci test\n')
