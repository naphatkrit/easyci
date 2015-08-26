import mock
import os

from click.testing import CliRunner

from easyci.cli import cli


def test_test_simple():
    def test_cli_config_simple():
        runner = CliRunner()
        with runner.isolated_filesystem():
            assert not os.system('git init')
            with mock.patch('easyci.cli.load_user_config') as mocked:
                mocked.return_value = {'tests': ['true', 'false']}
                result = runner.invoke(cli, ['test'])
                assert result.exit_code == 0
                assert 'Passed' in result.output
                assert 'Failed' in result.output
