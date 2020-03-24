# Standard Library Imports
from abc import abstractclassmethod
import os, subprocess, shutil, inspect

# Third Party Imports

# Local Application Imports
from ..host import Host

class WebHost(Host):

    @classmethod
    def load_config_defaults(cls, configholder):

        configholder.load_webhost_defaults(cls.__name__)

    @classmethod
    def get_repo_names_and_locations(cls, configholder):

        configholder.webhost_func_load_additional_configs(cls.__name__, inspect.currentframe().f_code.co_name) # inspect.currentframe().f_code.co_name returns function name
        return cls._get_repo_names_and_locations(configholder)

    @abstractclassmethod
    def _get_repo_names_and_locations(cls, configholder):

        pass
