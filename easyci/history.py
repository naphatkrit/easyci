import os


class NotStagedError(Exception):
    pass


class AlreadyStagedError(Exception):
    pass


class AlreadyCommittedError(Exception):
    pass


def _get_committed_history_path(vcs):
    """Get the path to the file containing committed tests history

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        str - the path
    """
    return os.path.join(vcs.private_dir(), 'passed')


def _get_staged_history_path(vcs):
    """Get the path to the file containing staged tests history

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        str - the path
    """
    return os.path.join(vcs.private_dir(), 'in_progress')


def get_committed_signatures(vcs):
    """Get the list of committed signatures

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        list(basestring) - list of signatures
    """
    committed_path = _get_committed_history_path(vcs)
    known_signatures = []
    if os.path.exists(committed_path):
        with open(committed_path, 'r') as f:
            known_signatures = f.read().split()
    return known_signatures


def get_staged_signatures(vcs):
    """Get the list of staged signatures

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        list(basestring) - list of signatures
    """
    staged_path = _get_staged_history_path(vcs)
    known_signatures = []
    if os.path.exists(staged_path):
        with open(staged_path, 'r') as f:
            known_signatures = f.read().split()
    return known_signatures


def commit_signature(vcs, user_config, signature):
    """Add `signature` to the list of committed signatures

    The signature must already be staged

    Args:
        vcs (easyci.vcs.base.Vcs)
        user_config (dict)
        signature (basestring)

    Raises:
        NotStagedError
        AlreadyCommittedError
    """
    if signature not in get_staged_signatures(vcs):
        raise NotStagedError
    evidence_path = _get_committed_history_path(vcs)
    committed_signatures = get_committed_signatures(vcs)
    if signature in committed_signatures:
        raise AlreadyCommittedError
    committed_signatures.append(signature)
    string = '\n'.join(committed_signatures[-user_config['history_limit']:])
    with open(evidence_path, 'w') as f:
        f.write(string)
    unstage_signature(vcs, signature)


def stage_signature(vcs, signature):
    """Add `signature` to the list of staged signatures

    Args:
        vcs (easyci.vcs.base.Vcs)
        signature (basestring)

    Raises:
        AlreadyStagedError
    """
    evidence_path = _get_staged_history_path(vcs)
    staged = get_staged_signatures(vcs)
    if signature in staged:
        raise AlreadyStagedError
    staged.append(signature)
    string = '\n'.join(staged)
    with open(evidence_path, 'w') as f:
        f.write(string)


def unstage_signature(vcs, signature):
    """Remove `signature` from the list of staged signatures

    Args:
        vcs (easyci.vcs.base.Vcs)
        signature (basestring)

    Raises:
        NotStagedError
    """
    evidence_path = _get_staged_history_path(vcs)
    staged = get_staged_signatures(vcs)
    if signature not in staged:
        raise NotStagedError
    staged.remove(signature)
    string = '\n'.join(staged)
    with open(evidence_path, 'w') as f:
        f.write(string)


def clear_history(vcs):
    """Clear (committed) test run history from this project.

    Args:
        vcs (easyci.vcs.base.Vcs)
    """
    evidence_path = _get_committed_history_path(vcs)
    if os.path.exists(evidence_path):
        os.remove(evidence_path)
