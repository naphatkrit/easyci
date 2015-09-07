import mock
import os
import pytest

from easyci import exit_codes
from easyci.cli import cli
from easyci.history import stage_signature
from easyci.results import _get_results_directory
from easyci.vcs.base import Vcs


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


def test_gc_no_results(runner, fake_vcs):
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['gc'])
    assert result.exit_code == exit_codes.SUCCESS


def test_gc_with_results(runner, fake_vcs):
    stage_signature(fake_vcs, 'signature1')
    stage_signature(fake_vcs, 'signature2')
    os.makedirs(_get_results_directory(fake_vcs, 'signature1'))
    os.makedirs(_get_results_directory(fake_vcs, 'nonexistentsignature1'))
    with mock.patch('easyci.cli.GitVcs', new=lambda: fake_vcs):
        result = runner.invoke(cli, ['gc'])
    assert result.exit_code == exit_codes.SUCCESS
    assert os.path.exists(_get_results_directory(fake_vcs, 'signature1'))
    assert not os.path.exists(_get_results_directory(fake_vcs, 'nonexistentsignature1'))
