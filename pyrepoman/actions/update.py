"""The 'Update' action class module."""
# Standard Library Imports
import os
import subprocess

# Third Party Imports

# Local Application Imports
from pyrepoman.actions.action import Action
from util.message import Message


class Update(Action):
    """The 'Update' action class.

    This action 'updates/pulls' git repos. Does
    this for git repos in the current working
    directory.

    Attributes
    ----------
    HELP_DESC : str
        Description provided for an action when using
        -h/--help with no action provided.

    """

    HELP_DESC = "update all Git repos in your current directory from remote repos"

    def __init__(self):

        super().__init__()

    @classmethod
    def _modify_parser(cls, parser):
        """Update's modifications of its parser.

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
        return parser

    def run(self):
        """Updates git repos in the present working directory.

        Raises
        ------
        subprocess.CalledProcessError
            If the git repos to be updated directories
            do not have write access or if the .git directory
            in the working directory does not have write access.
        PermissionError
            If the present working directory
            does not have read or execute permissions. # TODO WINDOWS PERMISSIONS?

        """
        try:
            nonbare_repo_names = super()._get_pwd_local_nonbare_repo_names()
            for nonbare_repo_name in nonbare_repo_names:
                os.chdir(nonbare_repo_name)
                subprocess.run(["git", "pull"], check=True)
                os.chdir("..")
        except PermissionError as e:
            Message.print_permission_denied(e.filename)
            raise
        except FileNotFoundError as e:
            Message.print_file_notfound(e.filename)
            raise
        except subprocess.CalledProcessError:
            os.chdir("..")
            # git pull forces program to eject before going back up the dir
            raise
