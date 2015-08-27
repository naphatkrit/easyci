import mock

from easyci.cli import cli


def test_test_simple_failed(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = {'tests': ['true', 'false']}
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == 1
    assert 'Passed' in result.output
    assert 'Failed' in result.output


def test_test_simple_passed(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = {'tests': ['true', 'true']}
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
    assert 'Passed' in result.output
    assert 'Failed' not in result.output
