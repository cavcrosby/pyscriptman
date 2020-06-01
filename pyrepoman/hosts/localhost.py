"""The 'LocalHost' host class module."""
# Standard Library Imports
import os
import pathlib
from os.path import expanduser

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host
from util.message import Message


class LocalHost(Host):
    """The 'Host' host class.

    This host allows you interact
    with your local system/machine.

    Parameters
    ----------
    configholder : util.configholder.ConfigHolder
        An instantiation of ConfigHolder, used to hold program configurations.

    Attributes
    ----------
    HELP_DESC : str
        Description provided for an host argument when using
        -h/--help with other arguments provided.
    PATH_CMD_ARG_NAME : str
        Chosen path is stored under this name.

    """
    HELP_DESC = "can manipulate local directories containing git repos"
    PATH_CMD_ARG_NAME = "path"

    def __init__(self, configholder):

        super().__init__()
        self.path = configholder.get_config_value(self.PATH_CMD_ARG_NAME)

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
        PermissionError
            If the present working directory has insufficient permissions
            and the dot character (alone anyways) is passed as
            the localhost argument. # TODO MAKE THIS AN EXAMPLE?

        """
        path = configholder.get_config_value(cls.PATH_CMD_ARG_NAME)
        path = "" if path == configholder.NON_EXISTANT_CONFIG else expanduser(path)

        try:
            return (
                chosen_host == cls._get_host_name() and pathlib.Path(path).exists()
            )
        except PermissionError as e:
            Message.print_permission_denied(e.filename)
            raise

    @classmethod
    def _modify_parser(cls, parser):
        """Allows the localhost parser to take custom arguments.

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
        parser.add_argument(
            cls.PATH_CMD_ARG_NAME, help="specifies what directory you wish to target"
        )

        return parser

    def get_user_repo_names_and_locations(self):
        """Used to determine repo names and locations for localhost.
        
        This method is the 'how' in getting
        the repo names and locations.

        Returns
        --------
        repo_names : list of str
            Git repo names are returned in a list. # TODO WHY NOT LOCATIONS?

        Raises
        --------
        PermissionError
            If the target directory (to pull repos from)
            does not have read or execute permissions. # TODO WINDOWS PERMISSIONS?

        """
        local_path = os.path.expanduser(self.path)
        try:
            repos = super()._get_bare_repo_names_from_path(local_path)
            for repo in repos:
                super().add_repo_name_and_location(repo, os.path.join(local_path, repo))
            return super().repo_names
        except PermissionError:
            raise
        except FileNotFoundError:
            raise
