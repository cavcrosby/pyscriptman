# Standard Library Imports
import sys

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message
from util.config import Config


class ConfigHolder:
    @property
    def NON_EXISTANT_CONFIG(self):

        return None

    @property
    def _DEFAULTS_ENTRY_NAME(self):

        return "defaults"

    def __init__(self, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        self.configs = list()
        self.CONFIGURATION_FILE_NAME = CONFIGURATION_FILE_NAME
        self.CONFIGURATION_FILE_PATH = CONFIGURATION_FILE_PATH

    @classmethod
    def from_object_dict(cls, obj, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        configholder = cls(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
        transformed_args = vars(obj)
        [
            configholder.add_config(arg, transformed_args[arg])
            for arg in transformed_args
        ]
        return configholder

    @staticmethod
    def _get_toml_table_entries(table, index):

        return table[index]

    def get_config(self, config_name):

        for config in self.configs:
            if config.name == config_name:
                return config

        return self.NON_EXISTANT_CONFIG

    def add_config(self, config_name, value):

        if self.config_exist(config_name):
            Message.print_configholder_duplicate_config_inserted(config_name, value)
            self.delete_config(config_name)
        self.configs.append(Config(config_name, value))

    def delete_config(self, config_name):

        if not self.config_exist(config_name):
            Message.print_configuration_not_exist(config_name)
            raise KeyError
        config = self.get_config(config_name)
        self.configs.remove(config)

    def config_exist(self, config_name):

        return self.get_config(config_name) != self.NON_EXISTANT_CONFIG

    def get_config_value(self, config_name):

        config = self.get_config(config_name)

        if config != self.NON_EXISTANT_CONFIG:
            return config.value

        return config

    def load_toml(self):

        try:
            self.add_config(
                self.CONFIGURATION_FILE_NAME, toml.load(self.CONFIGURATION_FILE_PATH)
            )
        except PermissionError as e:
            Message.print_permission_denied(e.filename)
            raise
        except toml.decoder.TomlDecodeError as e:  # thrown in: load_toml() if configuration file has syntax error
            Message.print_toml_decodeerror(e)
            raise

    def retrieve_table_defaults(self, table_name):

        tables = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            table_entries = self._get_toml_table_entries(tables, table_name)
        except KeyError:
            Message.print_table_not_exist(table_name)
            raise

        try:
            return self._get_toml_table_entries(
                table_entries, self._DEFAULTS_ENTRY_NAME
            )
        except KeyError:
            print(
                f"Error: {self._DEFAULTS_ENTRY_NAME} entry does not exist in the {table_name} table, check the configuration file"  # TODO PUT THIS IN MESSAGE CLASS
            )
            raise

    def table_func_retrieve_additional_configs(self, table_name, func_name):

        tables = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            table_entries = self._get_toml_table_entries(tables, table_name)
        except KeyError:
            Message.print_table_not_exist(table_name)
            raise
        if func_name not in table_entries:
            return type(tables)()
        elif (
            len(table_entries[func_name]) == 0
        ):  # empty [func_name] ... [another_func_name] key: value
            return type(tables)()
        else:
            return table_entries[func_name]

    def __str__(self):

        debug_configs_names = ["path", "host", "host_path"]
        return str(
            {
                debug_configs_name: self.get_config_value(debug_configs_name)
                for debug_configs_name in debug_configs_names
                if self.get_config_value(debug_configs_name) != self.NON_EXISTANT_CONFIG
            }
        )
