import mock
import pytest
import shutil
import tempfile

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
    fake_vcs.install_hook.assert_called_once_with(
        'pre-commit', '#!/bin/bash\neci test\n')
