# Standard Library Imports

# Third Party Imports
import toml

# Local Application Imports
from .global_variables import TOML_FILE_NAME, TOML_FILE_PATH

class ConfigHolder:

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

        self.add_config(TOML_FILE_NAME, toml.load(TOML_FILE_PATH))

    def load_webhost_defaults(self, webhost_name):

        WEBHOSTS_ENTRIES = self.get_config_value(TOML_FILE_NAME)
        WBHOST_ENTRIES = self._get_toml_table_entrys(WEBHOSTS_ENTRIES, webhost_name)
        DEFAULT_CONFIGS = self._get_toml_table_entrys(WBHOST_ENTRIES, "defaults")
        for default_config in DEFAULT_CONFIGS:
            self.add_config(default_config, DEFAULT_CONFIGS[default_config])

    def webhost_func_load_additional_configs(self, webhost_name, func_name):

        WEBHOSTS_ENTRIES = self.get_config_value(TOML_FILE_NAME)
        WBHOST_ENTRIES = self._get_toml_table_entrys(WEBHOSTS_ENTRIES, webhost_name)
        if(func_name not in WBHOST_ENTRIES):
            pass
        elif (len(WBHOST_ENTRIES[func_name]) == 0): # empty [func_name] ... [another_func_name] key: value
            pass
        else:
            FUNC_CONFIGS = WBHOST_ENTRIES[func_name]
            [self.add_config(config, FUNC_CONFIGS[config]) for config in FUNC_CONFIGS]

    def config_exist(self, config):

        if(self.get_config_value(config) != ""):
            return True

        return False

    def get_config_value(self, config):

        for pair in self.configs:
            if(pair[0] == config):
                return pair[1]

        return ""

    def __str__(self):
        
        return str(self.configs)
