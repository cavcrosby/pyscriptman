# Standard Library Imports
import os, subprocess, sys, re

# Third Party Imports

# Local Application Imports
from pyrepoman.actions.action import Action


class Update(Action):

    HELP_DESC = "update all Git repos in your current directory from remote repos"

    def __init__(self):

        super().__init__()

    @classmethod
    def _modify_parser(cls, parser):

        return parser

    def run(self):

        nonbare_repo_names = super()._get_pwd_local_nonbare_repo_names()
        for nonbare_repo_name in nonbare_repo_names:
            os.chdir(nonbare_repo_name)
            completed_process = subprocess.run(
                ["git", "pull"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding="utf-8",
            )
            os.chdir("..")
            completed_process.check_returncode()
