import mock
import os

from easyci.cli import cli
from easyci.user_config import ConfigFormatError, ConfigNotFoundError


def test_cli_config_not_found(runner, fake_hooks):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.side_effect = ConfigNotFoundError
        result = runner.invoke(cli, ['init'])
    assert result.exit_code == 0


def test_cli_config_format_error(runner, fake_hooks):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.side_effect = ConfigFormatError
        result = runner.invoke(cli, ['init'])
    assert result.exit_code != 0


def test_cli_config_simple(runner, fake_hooks):
    result = runner.invoke(cli, ['init'])
    assert result.exit_code == 0


def test_version_not_installed(runner):
    result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0

    runner.invoke(cli, ['init'])
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0


def test_version_mismatch(runner, fake_hooks):
    os.system('touch .git/eci/version')
    result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0
    assert 'mismatch' in result.output

    runner.invoke(cli, ['init'])
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
