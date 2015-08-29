import os


def _get_history_path(vcs):
    """Get the path to the file containing tests history

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        str - the path
    """
    return os.path.join(vcs.private_dir(), 'passed')


def get_known_signatures(vcs):
    """Get the list of signatures known to pass tests

    Args:
        vcs (easyci.vcs.base.Vcs)

    Returns:
        list(basestring) - list of signatures
    """
    evidence_path = _get_history_path(vcs)
    known_signatures = []
    if os.path.exists(evidence_path):
        with open(evidence_path, 'r') as f:
            known_signatures = f.read().split()
    return known_signatures


def add_signature(vcs, user_config, signature):
    """Add `signature` to the list of known signatures

    Args:
        vcs (easyci.vcs.base.Vcs)
        user_config (dict)
        signature (basestring)
    """
    evidence_path = _get_history_path(vcs)
    known_signatures = get_known_signatures(vcs)
    known_signatures.append(signature)
    string = '\n'.join(known_signatures[-user_config['history_limit']:])
    with open(evidence_path, 'w') as f:
        f.write(string)
