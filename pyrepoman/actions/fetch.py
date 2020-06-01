"""The 'Fetch' action class module."""
# Standard Library Imports
import subprocess

# Third Party Imports
import requests

# Local Application Imports
from util.message import Message
from pyrepoman.hosts.webhosts import github
from pyrepoman.actions.action import Action
from pyrepoman.pyrepoman_variables import REQUIRE_SUBCOMMANDS
from pyrepoman.hosts import (
    localhost,
    remotehost,
)


class Fetch(Action):
    """The 'Fetch' action class.

    This action clone git repos from a specified target
    and directory if applicable. This action requires
    a host object to communicate to.

    Parameters
    ----------
    host : pyrepoman.hosts.host.Host
        An instantiated Host object to be used by the action.

    Attributes
    ----------
    HELP_DESC : str
        Description provided for an action when using
        -h/--help with no action provided.

    """
    HELP_DESC = "fetch all Git repos through a web provider"

    def __init__(self, host):

        super().__init__()
        self.host = host

    @classmethod
    def _modify_parser(cls, parser):
        """Fetch's modifications of its parser.

        Supports GitHub, LocalHost, and RemoteHost hosts.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can take additional positional/optional arguments.

        """
        fetch_host_subparsers = parser.add_subparsers(
            title=cls._HOST_SUBPARSERS_TITLE, metavar=cls._HOST_SUBPARSER_METAVAR
        )
        fetch_host_subparsers.required = REQUIRE_SUBCOMMANDS
        github.GitHub.add_parser(fetch_host_subparsers, github.GitHub.HELP_DESC)
        remotehost.RemoteHost.add_parser(
            fetch_host_subparsers, remotehost.RemoteHost.HELP_DESC
        )
        localhost.LocalHost.add_parser(
            fetch_host_subparsers, localhost.LocalHost.HELP_DESC
        )
        return parser

    def run(self):
        """Clones git repos from a specified target and directory if applicable.

        Raises
        --------
        subprocess.CalledProcessError
            If the user chooses to communicate with
            a remotehost and the program fails to
            have communcations to the remotehost.
        PermissionError
            If the target directory (to pull repos from)
            does not have read or execute permissions. # TODO WINDOWS PERMISSIONS?

        """
        try:
            repo_names = self.host.get_user_repo_names_and_locations()
            for repo_name in repo_names:
                subprocess.run(
                    [
                        "git",
                        "clone",
                        f"{self.host.get_location_from_repo_name(repo_name)}",
                        f"{repo_name}",
                    ],
                    check=True,
                )
        except subprocess.CalledProcessError:
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
