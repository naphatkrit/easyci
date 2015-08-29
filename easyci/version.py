import os


class VersionNotInstalledError(Exception):
    pass


def _get_version_path(vcs):
    return os.path.join(vcs.private_dir(), 'version')


def get_installed_version(vcs):
    """Get the installed version for this project.

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        str - version number

    Raises:
        VersionNotInstalledError
    """
    version_path = _get_version_path(vcs)
    if not os.path.exists(version_path):
        raise VersionNotInstalledError
    with open(version_path, 'r') as f:
        return f.read().strip()


def set_installed_version(vcs, version):
    """Set the installed version for this project.

    Args:
        vcs (easyci.vcs.base.Vcs)
        version (str)
    """
    version_path = _get_version_path(vcs)
    with open(version_path, 'w') as f:
        f.write(version)
