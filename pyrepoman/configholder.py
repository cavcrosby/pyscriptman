# Standard Library Imports

# Third Party Imports
import toml

# Local Application Imports
from .global_variables import TOML_FILE_NAME, TOML_FILE_PATH

class ConfigHolder:

    @property
    def EMPTY_CONFIG(self):

        return ""

    def __init__(self, args):

        self.configs = list()
        transformed_args = vars(args)
        [self.add_config(arg, transformed_args[arg]) for arg in transformed_args]

    @staticmethod
    def _get_toml_table_entrys(toml, index):

        return toml[index]

    def add_config(self, key, value):

        """ ADD KEY/VALUE TUPLE TO A DATA STRUCTURE (config,value) """

        self.configs.append((key, value))

    def load_toml(self):

        # TODO EXCEPTION HANDLING WHEN FAIL TO LOAD TOML FILE?

        self.add_config(TOML_FILE_NAME, toml.load(TOML_FILE_PATH))

    def load_webhost_defaults(self, webhost_name):

        WEBHOSTS_ENTRIES = self.get_config_value(TOML_FILE_NAME)
        WBHOST_ENTRIES = self._get_toml_table_entrys(WEBHOSTS_ENTRIES, webhost_name)
        return self._get_toml_table_entrys(WBHOST_ENTRIES, "defaults")

    def webhost_func_load_additional_configs(self, webhost_name, func_name):

        WEBHOSTS_ENTRIES = self.get_config_value(TOML_FILE_NAME)
        WBHOST_ENTRIES = self._get_toml_table_entrys(WEBHOSTS_ENTRIES, webhost_name)
        if(func_name not in WBHOST_ENTRIES):
            return type(WEBHOSTS_ENTRIES)()
        elif (len(WBHOST_ENTRIES[func_name]) == 0): # empty [func_name] ... [another_func_name] key: value
            return type(WEBHOSTS_ENTRIES)()
        else:
            return WBHOST_ENTRIES[func_name]

    def config_exist(self, config):

        if(self.get_config_value(config) != self.EMPTY_CONFIG):
            return True

        return False

    def get_config_value(self, config):

        for pair in self.configs:
            if(pair[0] == config):
                return pair[1]

        return self.EMPTY_CONFIG

    def __str__(self):
        
        return str(self.configs)
