import os
import pytest

from easyci.results import (
    _get_results_directory, save_results, sync_results,
    ResultsNotFoundError, get_signatures_with_results,
    remove_results
)
from easyci.vcs.base import Vcs
from easyci.utils import contextmanagers


class DummyVcs(Vcs):

    def ignore_patterns_file(self):
        return '.dummyignore'

    def private_dir(self):
        return os.path.join(self.path, '.dummy/eci')


@pytest.yield_fixture(scope='function')
def vcs():
    with contextmanagers.temp_dir() as temp_dir:
        os.makedirs(os.path.join(temp_dir, '.dummy/eci'))
        yield DummyVcs(path=temp_dir)


def test_save_results(vcs):
    with vcs.temp_copy() as copy:
        with contextmanagers.chdir(copy.path):
            os.mkdir('dir')
            assert not os.system('touch a b c dir/a dir/b dir/c')
        save_results(vcs, 'signature1', copy.path, ['dir/***', 'a'])
    with contextmanagers.chdir(_get_results_directory(vcs, 'signature1')):
        assert os.path.exists('results/dir/a')
        assert os.path.exists('results/dir/b')
        assert os.path.exists('results/dir/c')
        assert os.path.exists('results/a')
        assert not os.path.exists('results/b')
        assert not os.path.exists('results/c')
        with open('patterns', 'r') as f:
            assert set(f.read().strip().split()) == set(['dir/***', 'a'])


def test_sync_results(vcs):
    results_dir = _get_results_directory(vcs, 'signature1')
    os.makedirs(results_dir)
    with contextmanagers.chdir(results_dir):
        with open('patterns', 'w') as f:
            f.write('\n'.join(['dir/***', 'a']))
        os.mkdir('results')
        with contextmanagers.chdir('results'):
            os.mkdir('dir')
            assert not os.system('touch a dir/a dir/b dir/c')
    with contextmanagers.chdir(vcs.path):
        assert not os.system('touch b c')
        with open('a', 'w') as f:
            f.write('testing')
    sync_results(vcs, 'signature1')
    with contextmanagers.chdir(vcs.path):
        assert os.path.exists('dir/a')
        assert os.path.exists('dir/b')
        assert os.path.exists('dir/c')
        assert os.path.exists('a')
        assert os.path.exists('b')
        assert os.path.exists('c')
        with open('a', 'r') as f:
            assert f.read() == ''


def test_sync_results_not_found(vcs):
    with pytest.raises(ResultsNotFoundError):
        sync_results(vcs, 'signature1')


def test_remove_results(vcs):
    # empty case
    with pytest.raises(ResultsNotFoundError):
        remove_results(vcs, 'signature1')

    # non-empty case
    results_dir = _get_results_directory(vcs, 'signature1')
    os.makedirs(results_dir)
    assert not os.system('touch {}'.format(os.path.join(results_dir, 'a')))
    remove_results(vcs, 'signature1')
    assert not os.path.exists(results_dir)


def test_get_signatures_with_results(vcs):
    assert get_signatures_with_results(vcs) == []

    os.makedirs(_get_results_directory(vcs, 'signature1'))
    assert get_signatures_with_results(vcs) == ['signature1']

    os.makedirs(_get_results_directory(vcs, 'signature2'))
    assert set(get_signatures_with_results(vcs)) == set(
        ['signature1', 'signature2'])
