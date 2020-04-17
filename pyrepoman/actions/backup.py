# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts import *
from pyrepoman.hosts.webhosts import *
from pyrepoman.actions.action import Action


class Backup(Action):

    HELP_DESC = "backup all Git repos, done by mirroring repos fully"

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.dest = configholder.get_config_value("dest")

    @classmethod
    def _modify_parser(cls, parser):

        parser.add_argument("dest", help="where to store backups (destination)")
        backup_host_subparsers = parser.add_subparsers(
            title=cls._HOST_SUBPARSER_TITLE, metavar=cls._HOST_SUBPARSER_TITLE
        )
        backup_host_subparsers.required = cls._REQUIRE_SUBCOMMANDS
        github.GitHub.add_parser(backup_host_subparsers, github.GitHub.HELP_DESC)
        remotehost.RemoteHost.add_parser(
            backup_host_subparsers, remotehost.RemoteHost.HELP_DESC
        )
        localhost.LocalHost.add_parser(
            backup_host_subparsers, localhost.LocalHost.HELP_DESC
        )
        return parser

    def run(self):

        repo_names_and_locations = self.host.get_user_repo_names_and_locations()
        dest = self.dest
        super()._create_dir(dest)
        not_delete = list()
        backup_content = os.listdir(dest)
        for repo_name in repo_names_and_locations:
            backup_repo_location = os.path.join(dest, repo_name)
            if not repo_name in backup_content:
                super()._create_mirror(
                    self.host.get_location_from_repo_name(repo_name),
                    backup_repo_location,
                )
            not_delete.append(repo_name)
        super()._remove_all_dir_content(dest, not_delete)
