import mock
import os
import pytest

from easyci import exit_codes
from easyci.cli import cli
from easyci.history import stage_signature, commit_signature
from easyci.user_config import ConfigFormatError, ConfigNotFoundError
from easyci.vcs.git import GitVcs


@pytest.fixture(scope='function', autouse=True)
def init(runner):
    result = runner.invoke(cli, ['init'])
    assert result.exit_code == exit_codes.SUCCESS


def test_config_not_found(runner, fake_hooks):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.side_effect = ConfigNotFoundError
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS


def test_config_format_error(runner, fake_hooks):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.side_effect = ConfigFormatError
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.FAILURE


def test_test_simple_failed(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'false'],
            'history_limit': 1,
            'collect_results': [],
        }
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.FAILURE
    assert 'Passed' in result.output
    assert 'Failed' in result.output


def test_test_simple_passed(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
            'collect_results': [],
        }
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'Passed' in result.output
    assert 'Failed' not in result.output


def test_run_twice(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
            'collect_results': [],
        }
        result = runner.invoke(cli, ['test'])
        assert result.exit_code == exit_codes.SUCCESS
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'OK' in result.output


def test_staged_only(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
            'collect_results': [],
        }
        assert not os.system('touch a && git add a && echo a > a')
        result = runner.invoke(cli, ['test', '--staged-only'])
        assert result.exit_code == exit_codes.SUCCESS
        assert not os.system('rm -f a && touch a')
        result = runner.invoke(cli, ['test', '--staged-only'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'OK' in result.output


def test_head_only(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
            'collect_results': [],
        }
        result = runner.invoke(cli, ['test'])
        assert result.exit_code == exit_codes.SUCCESS
        assert not os.system('touch a && git add a')
        assert not os.system('touch b')
        result = runner.invoke(cli, ['test', '--head-only'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'OK' in result.output


def test_run_twice_new_file(runner):
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': 1,
            'collect_results': [],
        }
        assert not os.system('touch a')
        result = runner.invoke(cli, ['test'])
        assert result.exit_code == exit_codes.SUCCESS
        assert not os.system('git add a')
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'OK' in result.output


def test_history_limit(runner):
    history_limit = 5
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['true', 'true'],
            'history_limit': history_limit,
            'collect_results': [],
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


def test_collect_results(runner):
    files = ['a.txt1', 'b.txt1', 'c.txt1']
    result_files = ['a.txt', 'b.txt', 'c.txt']
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = {
            'tests': ['touch ' + ' '.join(result_files + files)],
            'history_limit': 0,
            'collect_results': ['*.txt'],
        }
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS
    for f in files:
        assert not os.path.exists(f)
    for f in result_files:
        assert os.path.exists(f)


def test_already_staged_or_committed(runner):
    config = {
        'tests': ['true', 'true'],
        'history_limit': 1,
        'collect_results': [],
    }
    git = GitVcs()
    signature = git.get_signature()

    # test staged
    stage_signature(git, signature)
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = config
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.ALREADY_RUNNING
    assert 'In Progress' in result.output

    # test committed
    commit_signature(git, config, signature)
    with mock.patch('easyci.commands.test.load_user_config') as mocked:
        mocked.return_value = config
        result = runner.invoke(cli, ['test'])
    assert result.exit_code == exit_codes.SUCCESS
    assert 'OK' in result.output
