import mock
import os
import pytest
import shutil
import tempfile
import yaml

from easyci.vcs.base import Vcs
from easyci.user_config import (
    _config_types, _default_config, load_user_config,
    ConfigFormatError, ConfigNotFoundError
)


@pytest.yield_fixture(scope='function')
def repo_path():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _create_config_file(config, path):
    with open(os.path.join(path, 'eci.yaml'), 'w') as f:
        f.write(yaml.safe_dump(config))


@pytest.fixture(scope='function')
def fake_vcs(repo_path):
    vcs = mock.Mock(spec=Vcs)
    vcs.path = repo_path
    return vcs


def test_default_config_types():
    for k, v in _config_types.iteritems():
        if k in _default_config:
            assert isinstance(_default_config[k], v)


@pytest.mark.parametrize('tests', [
    ['true'],
    [],
    ['true', 'true'],
])
def test_load_user_config_simple(tests, fake_vcs, repo_path):
    _create_config_file({
        "tests": tests
    }, repo_path)
    config = load_user_config(fake_vcs)
    assert config['tests'] == tests


@pytest.mark.parametrize('user_config', [
    {},
    {"other": 0},
])
def test_load_user_config_default_config(user_config, fake_vcs, repo_path):
    _create_config_file(user_config, repo_path)
    config = load_user_config(fake_vcs)
    user_config.update(_default_config)
    assert config == user_config


@pytest.mark.parametrize('config_string', [
    yaml.safe_dump({}) + '}}',
    yaml.safe_dump({'tests': True}),
    yaml.safe_dump([]),
])
def test_load_user_config_invalid_config(config_string, fake_vcs, repo_path):
    with open(os.path.join(repo_path, 'eci.yaml'), 'w') as f:
        f.write(config_string)
    with pytest.raises(ConfigFormatError):
        load_user_config(fake_vcs)


def test_load_user_config_not_found(fake_vcs):
    with pytest.raises(ConfigNotFoundError):
        load_user_config(fake_vcs)
