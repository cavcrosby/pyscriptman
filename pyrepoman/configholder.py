# Standard Library Imports

# Third Party Imports
import toml

# Local Application Imports
from .global_variables import (
    TOML_FILE_NAME,
    TOML_FILE_PATH,
)


class ConfigHolder:
    @property
    def _EMPTY_CONFIG(self):

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

        try:
            self.add_config(TOML_FILE_NAME, toml.load(TOML_FILE_PATH))
        except PermissionError:
            raise OSError(
                13,
                "Error: Permission denied, cannot read configuration file",
                TOML_FILE_PATH,
            )
        except toml.decoder.TomlDecodeError as e:  # thrown in: load_toml() if configuration file has bad syntax error
            print(
                "Error: the configuration file contains syntax error(s), more details below"
            )
            print(e)
            raise SystemExit()

    def load_webhost_defaults(self, webhost_name):

        webhost_entries = self.get_config_value(TOML_FILE_NAME)
        try:
            wbhost_entries = self._get_toml_table_entrys(webhost_entries, webhost_name)
        except KeyError:
            print(
                f"Error: {webhost_name} table does not exist in the configuration file"
            )
            raise SystemExit()

        try:
            return self._get_toml_table_entrys(wbhost_entries, "defaults")
        except KeyError:
            print(
                f"Error: defaults table does not exist in the {webhost_name} table, check the configuration file"
            )
            raise SystemExit()

    def webhost_func_load_additional_configs(self, webhost_name, func_name):

        webhost_entries = self.get_config_value(TOML_FILE_NAME)
        try:
            wbhost_entries = self._get_toml_table_entrys(webhost_entries, webhost_name)
        except KeyError:
            print(
                f"Error: {webhost_name} table does not exist in the configuration file"
            )
            raise SystemExit()
        if func_name not in wbhost_entries:
            return type(webhost_entries)()
        elif (
            len(wbhost_entries[func_name]) == 0
        ):  # empty [func_name] ... [another_func_name] key: value
            return type(webhost_entries)()
        else:
            return wbhost_entries[func_name]

    def config_exist(self, config):

        return self.get_config_value(config) != self._EMPTY_CONFIG

    def get_config_value(self, config):

        for pair in self.configs:
            if pair[0] == config:
                return pair[1]

        return self._EMPTY_CONFIG

    def __str__(self):

        debug_configs = ["path", "host", "host_path"]
        return str(
            {
                debug_config: self.get_config_value(debug_config)
                for debug_config in debug_configs
                if self.get_config_value(debug_config) != self._EMPTY_CONFIG
            }
        )
