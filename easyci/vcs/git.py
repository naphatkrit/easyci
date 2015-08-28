import hashlib
import os
import stat

from easyci.vcs.base import CommandError, Vcs


class GitVcs(Vcs):
    binary_path = 'git'

    def __init__(self, path=None):
        super(GitVcs, self).__init__(path)
        private_dir = self.private_dir()
        if not os.path.exists(private_dir):
            os.makedirs(private_dir)

    def get_working_directory(self):
        """Get the working directory for this repo.

        This is available as a class method as it is usually needed to
        initialize the VCS object itself.

        Args:
            cls (class object): The class

        Returns:
            str - the path to the working directory

        Raises:
            CommandError
        """
        return self.run('rev-parse', '--show-toplevel').strip()

    def run(self, *cmd, **kwargs):
        cmd = [self.binary_path] + list(cmd)
        return super(GitVcs, self).run(*cmd, **kwargs)

    def remove_ignored_files(self):
        """Remove files ignored by the repository
        """
        self.run('clean', '-fdX')

    def remove_unstaged_files(self):
        """Remove all unstaged files. This does NOT remove ignored files.

        TODO this may be specific to git?
        """
        self.run('clean', '-fd')  # remove untracked files
        self.run('checkout', self.path)  # revert changes to staged version

    def private_dir(self):
        """Get the private directory associated with this repo, but untracked
        by the repo.

        Returns:
            str - path
        """
        return os.path.join(self.path, '.git/eci')

    def get_signature(self, base_commit=None):
        """Get the signature of the current state of the repository

        TODO right now `get_signature` is an effectful process in that
        it adds all untracked file to staging. This is the only way to get
        accruate diff on new files. This is ok because we only use it on a
        disposable copy of the repo.

        Args:
            base_commit - the base commit ('HEAD', sha, etc.)

        Returns:
            str
        """
        if base_commit is None:
            base_commit = 'HEAD'
        self.run('add', '-A', self.path)
        sha = self.run('rev-parse', '--verify', base_commit).strip()
        diff = self.run('diff', sha).strip()
        if len(diff) == 0:
            try:
                return self.get_signature(base_commit + '~1')
            except CommandError:
                pass
        h = hashlib.sha1()
        h.update(sha)
        h.update(diff)
        return h.hexdigest()

    def install_hook(self, hook_name, hook_content):
        """Install the repository hook for this repo.

        Args:
            hook_name (str)
            hook_content (str)
        """
        hook_path = os.path.join(self.path, '.git/hooks', hook_name)
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        os.chmod(hook_path, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
