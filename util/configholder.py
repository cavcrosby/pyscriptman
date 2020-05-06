# Standard Library Imports
import sys

# Third Party Imports
import toml

# Local Application Imports
from util.printexception import PrintException
from util.config import Config


class ConfigHolder:
    @property
    def EMPTY_CONFIG(self):

        return None

    @property
    def _DEFAULTS_ENTRY_NAME(self):

        return "defaults"

    def __init__(self, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        self.configs = list()
        self.CONFIGURATION_FILE_NAME = CONFIGURATION_FILE_NAME
        self.CONFIGURATION_FILE_PATH = CONFIGURATION_FILE_PATH

    @classmethod
    def from_object_dict(cls, args, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        configholder = cls(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
        transformed_args = vars(args)
        [
            configholder.add_config(arg, transformed_args[arg])
            for arg in transformed_args
        ]
        return configholder

    @staticmethod
    def _get_toml_table_entries(toml, index):

        return toml[index]

    def add_config(self, name, value):

        self.configs.append(Config(name, value))

    def load_toml(self):

        try:
            self.add_config(
                self.CONFIGURATION_FILE_NAME, toml.load(self.CONFIGURATION_FILE_PATH)
            )
        except PermissionError as e:
            PrintException.print_permission_denied(e.filename)
            raise
        except toml.decoder.TomlDecodeError as e:  # thrown in: load_toml() if configuration file has bad syntax error
            PrintException.print_toml_decodeerror(e)
            raise

    def retrieve_table_defaults(self, table_name):

        tables = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            table_entries = self._get_toml_table_entries(tables, table_name)
        except KeyError:
            PrintException.print_key_error(table_name)
            raise

        try:
            return self._get_toml_table_entries(
                table_entries, self._DEFAULTS_ENTRY_NAME
            )
        except KeyError:
            print(
                f"Error: {self._DEFAULTS_ENTRY_NAME} entry does not exist in the {table_name} table, check the configuration file"
            )
            raise

    def table_func_retrieve_additional_configs(self, table_name, func_name):

        tables = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            table_entries = self._get_toml_table_entries(tables, table_name)
        except KeyError:
            PrintException.print_key_error(table_name)
            raise
        if func_name not in table_entries:
            return type(tables)()
        elif (
            len(table_entries[func_name]) == 0
        ):  # empty [func_name] ... [another_func_name] key: value
            return type(tables)()
        else:
            return table_entries[func_name]

    def config_exist(self, config):

        return self.get_config_value(config) != self.EMPTY_CONFIG

    def get_config_value(self, config_name):

        for config in self.configs:
            if config.NAME == config_name:
                return config.VALUE

        return self.EMPTY_CONFIG

    def __str__(self):

        debug_configs_names = ["path", "host", "host_path"]
        return str(
            {
                debug_configs_name: self.get_config_value(debug_configs_name)
                for debug_configs_name in debug_configs_names
                if self.get_config_value(debug_configs_name) != self.EMPTY_CONFIG
            }
        )
