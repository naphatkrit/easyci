import mock
import os
import pytest

from easyci.vcs.base import Vcs


class DummyVcs(Vcs):
    def get_working_directory(self):
        return os.getcwd()


def test_init_with_path():
    path = '/dummy'
    with mock.patch('os.path.exists') as mocked:
        mocked.return_value = True
        vcs = Vcs(path=path)
        assert vcs.path == path

        mocked.return_value = False
        with pytest.raises(AssertionError):
            Vcs(path=path)


def test_init_without_path():
    path = '/dummy'
    with mock.patch('easyci.vcs.base.Vcs.get_working_directory') as mocked:
        mocked.return_value = path
        with mock.patch('os.path.exists') as path_mocked:
            path_mocked.return_value = True
            vcs = Vcs()
            assert vcs.path == path

            path_mocked.return_value = False
            with pytest.raises(AssertionError):
                Vcs()


def test_temp_copy():
    vcs = DummyVcs()
    with vcs.temp_copy() as copy:
        assert isinstance(copy, DummyVcs)
        assert copy.path != vcs.path
        assert os.path.exists(copy.path)
    assert not os.path.exists(copy.path)
