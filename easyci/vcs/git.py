import os
import stat

from easyci.vcs.base import Vcs


class GitVcs(Vcs):
    binary_path = 'git'

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
