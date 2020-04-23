# Standard Library Imports
import os, subprocess, sys, re

# Third Party Imports

# Local Application Imports
from pyrepoman.actions.action import Action
from pyrepoman.helpers import print_permission_denied, print_file_notfound


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
                completed_process = subprocess.run(["git", "pull"])
                os.chdir("..")
                completed_process.check_returncode()
        except PermissionError as e:
            print_permission_denied(e.filename)
            raise
        except FileNotFoundError as e:
            print_file_notfound(e.filename)
            raise
        except subprocess.CalledProcessError:
            raise
            
