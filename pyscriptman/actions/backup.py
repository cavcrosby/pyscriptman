"""The 'Backup' action class module."""
# Standard Library Imports
import subprocess
import shutil
import pathlib

# Third Party Imports
import requests

# Local Application Imports
from util.message import Message
from util.helpers import mirror_repo
from pyscriptman.hosts.webhosts import github
from pyscriptman.actions.action import Action
from pyscriptman.pyscriptman_variables import REQUIRE_SUBCOMMANDS
from pyscriptman.hosts import (
    localhost,
    remotehost,
)


class Backup(Action):
    """The 'Backup' action class.

    This action mirrors git repos from a specified target
    and directory if applicable. This action requires
    a host object to communicate to.

    Parameters
    ----------
    host : pyscriptman.hosts.host.Host
        An instantiated Host object to be used by the action.

    Attributes
    ----------
    HELP_DESC : str
        Description provided for an action when using
        -h/--help with no action provided.

    """

    HELP_DESC = "backup all Git repos, done by mirroring repos fully"

    def __init__(self, host):

        super().__init__()
        self.host = host

    @classmethod
    def _modify_parser(cls, parser):
        """Backup's modifications of its parser.

        Supports GitHub, LocalHost, and RemoteHost hosts.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can take additional positional/optional arguments.

        Returns
        -------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        """
        backup_host_subparsers = parser.add_subparsers(
            title=cls._HOST_SUBPARSERS_TITLE,
            metavar=cls._HOST_SUBPARSER_METAVAR,
        )
        backup_host_subparsers.required = REQUIRE_SUBCOMMANDS
        github.GitHub.add_parser(backup_host_subparsers)
        remotehost.RemoteHost.add_parser(backup_host_subparsers)
        localhost.LocalHost.add_parser(backup_host_subparsers)
        return parser

    def run(self):
        """Mirrors git repos from a specified target and directory if applicable.

        Raises
        ------
        subprocess.CalledProcessError
            If the user chooses to communicate with
            a remotehost and the program fails to
            have communcations to the remotehost.
        PermissionError
            If the target directory (to pull repos from)
            does not have read or execute permissions. # TODO DOES THIS APPLY FOR WINDOWS PERMISSIONS?

        """
        try:
            repo_names = self.host.get_user_repo_names_and_locations()
            for repo_name in repo_names:
                if(pathlib.Path(repo_name).exists()):
                    shutil.rmtree(repo_name)
                mirror_repo(
                    self.host.get_location_from_repo_name(repo_name),
                    repo_name,
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
