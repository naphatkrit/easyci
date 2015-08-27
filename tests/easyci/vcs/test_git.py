import os
import pytest
import shutil
import stat
import tempfile


from easyci.vcs.git import GitVcs


@pytest.yield_fixture(scope='function')
def repo_path():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


@pytest.fixture(scope='function')
def git(repo_path):
    assert not os.system('cd {path} && git init'.format(path=repo_path))
    return GitVcs(path=repo_path)


def test_get_working_directory(git, repo_path):
    path = git.get_working_directory()
    assert os.path.realpath(path) == os.path.realpath(repo_path)


def test_install_hook(git, repo_path):
    git.install_hook('pre-commit', '#!/bin/bash\ntrue\n')
    hook_path = os.path.join(repo_path, '.git/hooks/pre-commit')
    assert os.stat(hook_path).st_mode & 0777 == (
        stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE
    )
    with open(hook_path, 'r') as f:
        assert f.read() == '#!/bin/bash\ntrue\n'
