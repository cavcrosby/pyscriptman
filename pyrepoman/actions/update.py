# Standard Library Imports
import os, subprocess, sys, re

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
            stderr = subprocess.run(['git',  'pull'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stderr.rstrip()
            if(super()._permission_error(stderr)):
                raise OSError(13, 'Permission denied', nonbare_repo_name)
            os.chdir("..")
