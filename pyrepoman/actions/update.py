# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports
from .action import Action

class Update(Action):

    def __init__(self):

        super().__init__()

    def run(self):

        nonbare_repo_names = super()._get_pwd_local_nonbare_repo_names()
        for nonbare_repo_name in nonbare_repo_names:
            os.chdir(nonbare_repo_name)
            subprocess.run(["git",  "pull"])
            os.chdir("..")
