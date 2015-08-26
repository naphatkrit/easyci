import pytest
import mock

from easyci.vcs.base import Vcs


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
