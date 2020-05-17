# Standard Library Imports
from abc import abstractmethod
import os, subprocess, shutil, inspect

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host


class WebHost(Host):
    def __init__(self, configholder):
        super().__init__()
        self.configholder = configholder

    def load_config_defaults(self):

        default_configs = self.configholder.retrieve_table_defaults(
            self._get_host_name()
        )
        for default_config in default_configs:
            setattr(self, default_config, default_configs[default_config])

    def get_user_repo_names_and_locations(self):

        func_configs = self.configholder.table_func_retrieve_additional_configs(
            self._get_host_name(), inspect.currentframe().f_code.co_name
        )  # inspect.currentframe().f_code.co_name returns function name
        for func_config in func_configs:
            setattr(self, func_config, func_configs[func_config])
        return self._get_user_repo_names_and_locations()

    @abstractmethod
    def _get_user_repo_names_and_locations(self):

        pass
