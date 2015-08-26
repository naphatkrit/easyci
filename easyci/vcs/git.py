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
