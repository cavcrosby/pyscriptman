"""The 'RemoteHost' host class module."""
# Standard Library Imports
import subprocess

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host
from util.helpers import (
    copy_script_to_host,
    execute_script_on_host,
    remove_script_on_host,
    expand_target_path_on_host,
)
from global_variables import (
    REMOTE_SCRIPT_GET_BARE_REPOS_NAME,
    REMOTE_SCRIPT_GET_BARE_REPOS_PATH,
)


class RemoteHost(Host):
    """The 'RemoteHost' host class.

    This interface allows you to interact
    with a remote machine.

    Parameters
    ----------
    configholder : util.configholder.ConfigHolder
        An instantiation of ConfigHolder, used to hold program configurations.

    Attributes
    ----------
    HELP_DESC : str
        Parser description of RemoteHost
        when using -h/--help.
    TARGET_KEY : str
        Target is the user and machine. Format should be
        <user>@<ip address/url>.
    TARGET_PATH_KEY : str
        Path on the remote machine to check for bare
        Git repos.
    DEFAULT_TARGET_PATH : str
        Default path on remote machine to check
        for bare Git repos.
    """

    HELP_DESC = "can target directories on remote hosts"
    TARGET_KEY = "target"
    TARGET_PATH_KEY = "target_path"
    DEFAULT_TARGET_PATH = "$HOME"

    def __init__(self, configholder):

        super().__init__()
        self.target = configholder.get_config_value(self.TARGET_KEY)
        self.target_path = configholder.get_config_value(self.TARGET_PATH_KEY)

    @classmethod
    def is_host_type(cls, chosen_host, configholder):
        """How the host type is determined.
        
        Parameters
        ----------
        chosen_host : str
            Input received from the command line.
        configholder : util.configholder.ConfigHolder
            An instantiation of ConfigHolder, used to hold program configurations.
            
        Returns
        --------
        bool
            Whether or not the user has chosen this host type
            and that other requirements were also met for
            it to be this host type.

        Raises
        --------
        subprocess.CalledProcessError

            A generic error thrown by the subprocess
            library if the process (subprocess.run()) exits
            with a non-zero exit code. Below are the non-obvious errors
            known (or possibly) to be thrown.

            --> If either the target is unreachable.
            --> If the directory on the target does not exist.

        Examples
        ----------
        (pyrepoman) reap2sow1@Ron:~$ pyrepoman fetch -h # TODO FINALIZE EXAMPLE
        available hosts:
            host [options ...]
                [...]
                remotehost        can target directories on remote hosts

        """

        def can_reach_target(target):
            """To determine if target can be communicated with"""
            subprocess.run(
                ["ssh", target, "exit"], check=True,
            )
            return True

        def can_reach_remote_dir(target, target_path):
            """To determine if the remote directory exists on the target"""
            completed_process = subprocess.run(
                [
                    "ssh",
                    target,
                    f'python3 -c "import os; print(os.path.exists(\\"{target_path}\\"));"',
                ],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding="utf-8",
                check=True,
            )
            return completed_process.stdout.strip() == "True"

        if chosen_host != cls._get_host_name():
            return False
        try:
            target = configholder.get_config_value(cls.TARGET_KEY)
            expanded_path = expand_target_path_on_host(
                target, configholder.get_config_value(cls.TARGET_PATH_KEY)
            )
            return can_reach_target(target) and can_reach_remote_dir(
                target, expanded_path
            )
        except subprocess.CalledProcessError:
            raise

    @classmethod
    def _modify_parser(cls, parser):
        """Allows the remotehost parser to take custom arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        Returns
        --------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        """
        target_path_cmd_name_dash = cls.TARGET_PATH_KEY.replace("_", "-")

        parser.add_argument(
            cls.TARGET_KEY,
            help="specifies what host you wish to target, host format is the format of hostname in ssh",
        )
        parser.add_argument(
            f"--{target_path_cmd_name_dash}",
            metavar="path",
            default=cls.DEFAULT_TARGET_PATH,
            help=f"specifies what directory on the host to target for repos (default: {cls.DEFAULT_TARGET_PATH}).",
        )

        return parser

    def get_user_repo_names_and_locations(self):
        """Used to determine repo names and locations for remotehost.
        
        This method is the 'how' in getting
        the repo names and locations. Host
        object will store the locations of
        the repos.

        Returns
        --------
        repo_names : list of str
            Git repo names are returned in a list.

        Raises
        --------
        subprocess.CalledProcessError

            A generic error thrown by the subprocess
            library if the process (subprocess.run()) exits
            with a non-zero exit code. Below are the non-obvious errors known
            (or possibly) to be thrown.

            --> If either the target is unreachable.
            --> If the directory on the target does not exist.
            --> If the target directory does not have write/execute # TODO WINDOWS PERMISSIONS
            permissions.

        """
        target = self.target
        try:
            target_path = expand_target_path_on_host(target, self.target_path)
            remote_script_target_path = (
                f"{target_path}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
            )
            copy_script_to_host(target, target_path, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
            bare_repos = execute_script_on_host(
                target, target_path, remote_script_target_path
            )
            remove_script_on_host(target, remote_script_target_path)
            for repo in bare_repos:
                super().add_repo_name_and_location(
                    repo, f"{target}:{target_path}{repo}"
                )
            return super().repo_names
        except subprocess.CalledProcessError:
            raise
