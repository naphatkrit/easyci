import click
import os
import pytest

from easyci.cli import cli


@pytest.fixture(scope='function')
def fake_command():
    @click.command()
    def fake():
        click.echo('Fake!')
    cli.add_command(fake)
    return fake


def test_version_not_installed(runner, fake_command, fake_hooks):
    result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0

    runner.invoke(cli, ['init'])
    result = runner.invoke(cli, ['fake'])
    assert result.exit_code == 0


def test_version_mismatch(runner, fake_command, fake_hooks):
    os.system('touch .git/eci/version')
    result = runner.invoke(cli, ['test'])
    assert result.exit_code != 0
    assert 'mismatch' in result.output

    runner.invoke(cli, ['init'])
    result = runner.invoke(cli, ['fake'])
    assert result.exit_code == 0
