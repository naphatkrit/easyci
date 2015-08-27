import mock
import os

from easyci.cli import cli
from easyci.vcs.git import GitVcs


def test_test_simple_failed(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = mocked.return_value = {
            'tests': ['true', 'false'],
            'history_limit': 1,
        }
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == 1
    assert 'Passed' in result.output
    assert 'Failed' in result.output


def test_test_simple_passed(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
        }
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
    assert 'Passed' in result.output
    assert 'Failed' not in result.output


def test_run_twice(runner):
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
        }
        result = runner.invoke(cli, ['test'])
        assert result.exit_code == 0
        result = runner.invoke(cli, ['test'])
    assert 'OK' in result.output


def test_history_limit(runner):
    history_limit = 5
    with mock.patch('easyci.cli.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': history_limit,
        }
        for x in range(history_limit + 1):
            assert not os.system('touch {x} && git add {x}'.format(x=x))
            result = runner.invoke(cli, ['test'])
            assert result.exit_code == 0
            result = runner.invoke(cli, ['test'])
    git = GitVcs()
    evidence = os.path.join(git.private_dir(), 'passed')
    with open(evidence, 'r') as f:
        signatures = f.read().split()
        assert len(signatures) == history_limit
        assert signatures[-1] == git.get_signature()
