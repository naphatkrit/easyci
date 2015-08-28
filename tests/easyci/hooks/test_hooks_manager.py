import pytest

from easyci.hooks.hooks_manager import get_hook, HookNotFoundError


def test_get_hook():
    assert get_hook('pre-commit')

    with pytest.raises(HookNotFoundError):
        get_hook('doesnotexist')
