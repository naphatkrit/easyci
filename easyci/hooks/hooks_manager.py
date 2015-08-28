import pkg_resources


class HookNotFoundError(Exception):
    pass


def get_hook(hook_name):
    """Returns the specified hook.

    Args:
        hook_name (str)

    Returns:
        str - (the content of) the hook

    Raises:
        HookNotFoundError
    """
    if not pkg_resources.resource_exists(__name__, hook_name):
        raise HookNotFoundError
    return pkg_resources.resource_string(__name__, hook_name)
