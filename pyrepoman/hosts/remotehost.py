# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host
from util.printmessage import PrintMessage
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

    HELP_DESC = "can target directories on remote hosts"

    def __init__(self, configholder):

        super().__init__()
        self.target = configholder.get_config_value("target")
        self.target_path = configholder.get_config_value("target_path")

    @classmethod
    def is_host_type(cls, chosen_host, configholder):
        def can_reach_remote_dir(target, target_path):

            completed_process = subprocess.run(
                [
                    "ssh",
                    target,
                    f'python3 -c "import os; print(os.path.exists(\\"{target_path}\\"));"',
                ],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding="utf-8",
            )
            completed_process.check_returncode()
            return completed_process.stdout.strip() == "True"

        if chosen_host != cls._get_host_name():
            return False
        try:
            target = configholder.get_config_value("target")
            expanded_path = expand_target_path_on_host(
                target, configholder.get_config_value("target_path")
            )
            return can_reach_remote_dir(target, expanded_path)
        except subprocess.CalledProcessError:
            raise

    @classmethod
    def _modify_parser(cls, parser):

        default_target_path = "$HOME"

        parser.add_argument(
            "target",
            help="specifies what host you wish to target, host format is the format of hostname in ssh",
        )
        parser.add_argument(
            "--target-path",
            metavar="path",
            default=default_target_path,
            help=f"specifies what directory on the host to target for repos (default: {default_target_path}).",
        )

        return parser

    def get_user_repo_names_and_locations(self):

        target = self.target
        try:
            target_path = expand_target_path_on_host(
                target, self.target_path
            )  # target_path really is endpoint path we are looking to manipulate repos from
            remote_script_target_path = (
                f"{target_path}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
            )
            copy_script_to_host(target, target_path, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
            bare_repos = execute_script_on_host(
                target, remote_script_target_path
            )
            remove_script_on_host(target, remote_script_target_path)
            for repo in bare_repos:
                self.add_repo_name_and_location(repo, f"{target}:{target_path}{repo}")
            return self.repo_names_and_locations
        except subprocess.CalledProcessError:
            raise
