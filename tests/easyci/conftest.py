import os
import pytest

from click.testing import CliRunner


@pytest.yield_fixture(scope='function')
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        assert not os.system('git init')
        with open('eci.yaml', 'w') as f:
            f.write('{}')
        yield runner
