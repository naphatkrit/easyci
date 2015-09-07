import os
import subprocess32 as subprocess


class ResultsNotFoundError(Exception):
    pass


def _get_results_directory(vcs, signature):
    return os.path.join(vcs.private_dir(), 'results', signature)


def save_results(vcs, signature, result_path, patterns):
    """Save results matching `patterns` at `result_path`.

    Args:
        vcs (easyci.vcs.base.Vcs) - the VCS object for the actual project
                                    (not the disposable copy)
        signature (str) - the project state signature
        result_path (str) - the path containing the result, usually
                            a disposable copy of the project
        patterns (str) - `rsync`-compatible patterns matching test results
                         to save.
    """
    results_directory = _get_results_directory(vcs, signature)
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    with open(os.path.join(results_directory, 'patterns'), 'w') as f:
        f.write('\n'.join(patterns))
    if not os.path.exists(os.path.join(results_directory, 'results')):
        os.mkdir(os.path.join(results_directory, 'results'))
    includes = ['--include={}'.format(x)
                for x in patterns]
    cmd = ['rsync', '-r'] + includes + ['--exclude=*',
                                        os.path.join(result_path, ''),
                                        os.path.join(results_directory, 'results', '')]
    subprocess.check_call(cmd)


def sync_results(vcs, signature):
    """Sync the saved results for `signature` back to the project.

    Args:
        vcs (easyci.vcs.base.Vcs)
        signature (str)
    """
    results_directory = _get_results_directory(vcs, signature)
    if not os.path.exists(results_directory):
        raise ResultsNotFoundError
    with open(os.path.join(results_directory, 'patterns'), 'r') as f:
        patterns = f.read().strip().split()
    includes = ['--include={}'.format(x)
                for x in patterns]
    cmd = ['rsync', '-r'] + includes + ['--exclude=*',
                                        os.path.join(results_directory, 'results', ''),
                                        os.path.join(vcs.path, '')]
    subprocess.check_call(cmd)
