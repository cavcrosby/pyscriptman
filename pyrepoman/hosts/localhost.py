# Standard Library Imports
import os, subprocess, platform, pathlib, sys

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host


class LocalHost(Host):

    HELP_DESC = "can manipulate local directories containing git repos"

    def __init__(self, configholder):

        super().__init__()
        self.path = configholder.get_config_value("path")

    @classmethod
    def is_host_type(cls, identifier, configholder):

        path = os.path.expanduser(configholder.get_config_value("path"))

        try:
            return identifier == cls.__name__.lower() and pathlib.Path(path).exists()
        except PermissionError:
            raise OSError(13, "Error: Permission denied", path)

    @classmethod
    def _modify_parser(cls, parser):

        parser.add_argument("path", help="specifies what directory you wish to target")

        return parser

    def get_user_repo_names_and_locations(self):

        local_path = os.path.expanduser(self.path)
        repos = self._get_pwd_bare_repo_names(local_path)
        for repo in repos:
            self.add_repo_name_and_location(repo, os.path.join(local_path, repo))
        return self.repo_names_and_locations
