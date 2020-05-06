# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts import *
from pyrepoman.hosts.webhosts import *
from pyrepoman.actions.action import Action


class Archive(Action):

    HELP_DESC = "archive all Git repos, done by bundling repos"

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.dest = configholder.get_config_value("dest")
        self.tmp_dir = "archive_tmp"

    @classmethod
    def _modify_parser(cls, parser):

        parser.add_argument("dest", help="where to store archives (destination)")
        archive_host_subparsers = parser.add_subparsers(
            title=cls._HOST_SUBPARSER_TITLE, metavar=cls._HOST_SUBPARSER_TITLE
        )
        archive_host_subparsers.required = cls._REQUIRE_SUBCOMMANDS
        github.GitHub.add_parser(archive_host_subparsers, github.GitHub.HELP_DESC)
        remotehost.RemoteHost.add_parser(
            archive_host_subparsers, remotehost.RemoteHost.HELP_DESC
        )
        localhost.LocalHost.add_parser(
            archive_host_subparsers, localhost.LocalHost.HELP_DESC
        )
        return parser

    def run(self):

        repo_names_and_locations = self.host.get_user_repo_names_and_locations()
        dest, tmp_dir = self.dest, self.tmp_dir
        super()._create_dir(dest)
        super()._create_dir(tmp_dir)
        super()._remove_all_dir_content(dest)
        for repo_name in repo_names_and_locations:
            backup_repo_location = os.path.join(tmp_dir, repo_name)
            super()._create_mirror(
                self.host.get_location_from_repo_name(repo_name), backup_repo_location
            )
            super()._create_bundle(os.path.join(dest, repo_name), backup_repo_location)
        super()._remove_dir(tmp_dir)
