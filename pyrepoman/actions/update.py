# Standard Library Imports
import os
import subprocess

# Third Party Imports

# Local Application Imports
from pyrepoman.actions.action import Action
from util.message import Message


class Update(Action):

    HELP_DESC = "update all Git repos in your current directory from remote repos"

    def __init__(self):

        super().__init__()

    @classmethod
    def _modify_parser(cls, parser):

        return parser

    def run(self):

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
