import mock
import os
import pytest

from click.testing import CliRunner


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        os.mkdir('.git/eci')
        with open('eci.yaml', 'w') as f:
            f.write('{}')
        assert not os.system('git add eci.yaml && git commit -m "eci.yaml"')
        yield runner


@pytest.yield_fixture(scope='session')
def fake_hooks():
    with mock.patch('easyci.hooks.hooks_manager.get_hook', new=lambda x: x):
        yield
