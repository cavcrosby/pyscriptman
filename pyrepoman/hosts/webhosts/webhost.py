# Standard Library Imports
from abc import abstractmethod
import os, subprocess, shutil, inspect

# Third Party Imports

# Local Application Imports
from ..host import Host

class WebHost(Host):

    def load_config_defaults(self, configholder):

        DEFAULT_CONFIGS = configholder.load_webhost_defaults(type(self).__name__.lower())
        for default_config in DEFAULT_CONFIGS:
            setattr(self, default_config, DEFAULT_CONFIGS[default_config])

    def get_repo_names_and_locations(self, configholder):

        FUNC_CONFIGS = configholder.webhost_func_load_additional_configs(type(self).__name__.lower(), inspect.currentframe().f_code.co_name) # inspect.currentframe().f_code.co_name returns function name
        for func_config in FUNC_CONFIGS:
            setattr(self, func_config, FUNC_CONFIGS[func_config])
        return self._get_repo_names_and_locations()

    @abstractmethod
    def _get_repo_names_and_locations(self):

        pass
