import mock
import os

from click.testing import CliRunner

from easyci.cli import cli
from easyci.user_config import ConfigFormatError, ConfigNotFoundError


def test_cli_config_not_found():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        with mock.patch('easyci.cli.load_user_config') as mocked:
            mocked.side_effect = ConfigNotFoundError
            result = runner.invoke(cli, ['test'])
            assert result.exit_code != 0


def test_cli_config_format_error():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        with mock.patch('easyci.cli.load_user_config') as mocked:
            mocked.side_effect = ConfigFormatError
            result = runner.invoke(cli, ['test'])
            assert result.exit_code != 0


def test_cli_config_simple():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        with mock.patch('easyci.cli.load_user_config') as mocked:
            mocked.return_value = {'tests': []}
            result = runner.invoke(cli, ['test'])
            assert result.exit_code == 0
