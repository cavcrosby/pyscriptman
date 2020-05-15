# Standard Library Imports
import subprocess, os

# Third Party Imports
from requests.exceptions import ConnectionError, HTTPError

# Local Application Imports
from pyrepoman.hosts import *
from pyrepoman.hosts.webhosts import *
from pyrepoman.actions.action import Action
from util.printmessage import PrintMessage


class Fetch(Action):

    HELP_DESC = "fetch all Git repos through a web provider"

    def __init__(self, host):

        super().__init__()
        self.host = host

    @classmethod
    def _modify_parser(cls, parser):

        fetch_host_subparsers = parser.add_subparsers(
            title=cls._HOST_SUBPARSER_TITLE, metavar=cls._HOST_SUBPARSER_TITLE
        )
        fetch_host_subparsers.required = cls._REQUIRE_SUBCOMMANDS
        github.GitHub.add_parser(fetch_host_subparsers, github.GitHub.HELP_DESC)
        remotehost.RemoteHost.add_parser(
            fetch_host_subparsers, remotehost.RemoteHost.HELP_DESC
        )
        localhost.LocalHost.add_parser(
            fetch_host_subparsers, localhost.LocalHost.HELP_DESC
        )
        return parser

    def run(self):

        try:
            repo_names_and_locations = self.host.get_user_repo_names_and_locations()
            for repo_name in repo_names_and_locations:
                completed_process = subprocess.run(
                    [
                        "git",
                        "clone",
                        f"{self.host.get_location_from_repo_name(repo_name)}",
                        f"{repo_name}",
                    ],
                )
                completed_process.check_returncode()
        except subprocess.CalledProcessError:
            raise
        except PermissionError as e:
            PrintMessage.print_permission_denied(e.filename)
            raise
        except FileNotFoundError as e:
            PrintMessage.print_file_notfound(e.filename)
            raise
        except AttributeError:
            raise
        except ConnectionError:
            raise
        except HTTPError:
            raise
