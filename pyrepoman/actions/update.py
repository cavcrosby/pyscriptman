# Standard Library Imports
import os, subprocess, sys

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
            subprocess.run(["git",  "pull"]) # TODO, IF ACCESS IS DENIED TO THE REPO, WE SHOULD RAISE A PERMISSIONERROR EXCEPTION
            #PermissionError(filename=sys.modules[__name__])
            os.chdir("..")
