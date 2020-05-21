# Standard Library Imports
import subprocess

# Third Party Imports
import requests

# Local Application Imports
from pyrepoman.hosts import localhost, remotehost
from pyrepoman.hosts.webhosts import github
from pyrepoman.actions.action import Action
from util.message import Message
from util.helpers import bundle_repo


class Archive(Action):

    HELP_DESC = "archive all Git repos, done by bundling repos"

    def __init__(self, host):

        super().__init__()
        self.host = host

    @classmethod
    def _modify_parser(cls, parser):

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

        try:
            repo_names = self.host.get_user_repo_names_and_locations()
            for repo_name in repo_names:
                bundle_repo(self.host.get_location_from_repo_name(repo_name), repo_name)
        except subprocess.CalledProcessError as e:
            raise
        except PermissionError as e:
            Message.print_permission_denied(e.filename)
            raise
        except FileNotFoundError as e:
            Message.print_file_notfound(e.filename)
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.HTTPError:
            raise
