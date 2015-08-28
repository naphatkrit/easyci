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


@pytest.fixture(scope='function', params=[
    ['foo'],
    ['foo', 'bar'],
])
def git(repo_path, request):
    assert not os.system(
        'cd {path} && git init'.format(path=repo_path))
    for commit in request.param:
        assert not os.system(
            'cd {p} && touch {c} && git add {c} && git commit -m {c}'.format(p=repo_path, c=commit))
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


def test_remove_unstaged_files(git, repo_path):
    assert not os.system(
        'cd {} && touch a && git add a && echo 123 > a'.format(repo_path))
    assert not os.system('cd {} && touch b'.format(repo_path))

    assert os.path.exists(os.path.join(repo_path, 'a'))
    assert os.path.exists(os.path.join(repo_path, 'b'))
    with open(os.path.join(repo_path, 'a'), 'r') as f:
        assert f.read() == '123\n'
    git.remove_unstaged_files()
    assert not os.path.exists(os.path.join(repo_path, 'b'))
    with open(os.path.join(repo_path, 'a'), 'r') as f:
        assert f.read() == ''


def test_remove_ignored_files(git, repo_path):
    with open(os.path.join(repo_path, '.gitignore'), 'w') as f:
        f.write('a\nb\n')
    assert not os.system(
        'cd {} && touch a && mkdir b && touch b/testing'.format(repo_path))
    assert os.path.exists(os.path.join(repo_path, 'a'))
    assert os.path.exists(os.path.join(repo_path, 'b'))
    git.remove_ignored_files()
    assert not os.path.exists(os.path.join(repo_path, 'a'))
    assert not os.path.exists(os.path.join(repo_path, 'b'))


def test_get_signature(git, repo_path):
    git.get_signature()  # get signature works

    # check that get signature works with untracked files
    assert not os.system('cd {} && touch a'.format(repo_path))
    old_signature = git.get_signature()
    assert not os.system('cd {} && git add a'.format(repo_path))
    assert old_signature == git.get_signature()

    # check that we get a different signature by adding a new file
    assert not os.system('cd {} && touch b && git add b'.format(repo_path))
    new_signature = git.get_signature()
    assert old_signature != new_signature

    # bringing the repo back to the old structure retains the signature
    assert not os.system('cd {} && rm -f b && git rm b'.format(repo_path))
    assert git.get_signature() == old_signature

    # commiting does not change the signature
    assert not os.system('cd {} && git commit -m commit'.format(repo_path))
    assert git.get_signature() == old_signature


def test_private_dir(git, repo_path):
    private_dir = git.private_dir()
    assert os.path.join(repo_path, '.git/eci') == private_dir
    assert os.path.exists(private_dir)
    assert os.path.isdir(private_dir)
