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

    HELP_DESC = "can target directories on remote hosts"
    TARGET_CMD_ARG_NAME = "target"
    TARGET_PATH_CMD_ARG_NAME = "target_path"
    DEFAULT_TARGET_PATH = "$HOME"

    def __init__(self, configholder):

        super().__init__()
        self.target = configholder.get_config_value(self.TARGET_CMD_ARG_NAME)
        self.target_path = configholder.get_config_value(self.TARGET_PATH_CMD_ARG_NAME)

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
                check=True,
            )
            return completed_process.stdout.strip() == "True"

        if chosen_host != cls._get_host_name():
            return False
        try:
            target = configholder.get_config_value(cls.TARGET_CMD_ARG_NAME)
            expanded_path = expand_target_path_on_host(
                target, configholder.get_config_value(cls.TARGET_PATH_CMD_ARG_NAME)
            )
            return can_reach_remote_dir(target, expanded_path)
        except subprocess.CalledProcessError:
            raise

    @classmethod
    def _modify_parser(cls, parser):

        target_path_cmd_name_dash = cls.TARGET_PATH_CMD_ARG_NAME.replace("_", "-")

        parser.add_argument(
            cls.TARGET_CMD_ARG_NAME,
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

        target = self.target
        try:
            target_path = expand_target_path_on_host(
                target, self.target_path
            )
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
