import mock

from easyci.cli import cli
from easyci.user_config import ConfigFormatError, ConfigNotFoundError


def test_cli_config_not_found(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.side_effect = ConfigNotFoundError
        result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0


def test_cli_config_format_error(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.side_effect = ConfigFormatError
        result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0


def test_cli_config_simple(runner):
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
