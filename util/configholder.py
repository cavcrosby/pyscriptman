# Standard Library Imports
import sys

# Third Party Imports
import toml

# Local Application Imports
from pyrepoman.helpers import print_permission_denied


class ConfigHolder:
    @property
    def _EMPTY_CONFIG(self):

        return ""

    def __init__(self, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        self.configs = list()
        self.CONFIGURATION_FILE_NAME = CONFIGURATION_FILE_NAME
        self.CONFIGURATION_FILE_PATH = CONFIGURATION_FILE_PATH

    @staticmethod
    def _get_toml_table_entrys(toml, index):

        return toml[index]

    @classmethod
    def from_object_dict(cls, args, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        configholder = cls(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
        transformed_args = vars(args)
        [
            configholder.add_config(arg, transformed_args[arg])
            for arg in transformed_args
        ]
        return configholder

    def add_config(self, key, value):

        """ ADD KEY/VALUE TUPLE TO A DATA STRUCTURE (config,value) """

        self.configs.append((key, value))

    def load_toml(self):

        try:
            self.add_config(self.CONFIGURATION_FILE_NAME, toml.load(self.CONFIGURATION_FILE_PATH))
        except PermissionError as e:
            print_permission_denied(e.filename)
            sys.exit(e.errno)
        except toml.decoder.TomlDecodeError as e:  # thrown in: load_toml() if configuration file has bad syntax error
            print(
                "Error: the configuration file contains syntax error(s), more details below"
            )
            print(e)
            sys.exit()

    def retrieve_table_defaults(self, table_name):

        table_entries = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            tb_entries = self._get_toml_table_entrys(table_entries, table_name)
        except KeyError:
            print(
                f"Error: {table_name} table does not exist in the configuration file"
            )
            raise SystemExit()

        try:
            return self._get_toml_table_entrys(tb_entries, "defaults")
        except KeyError:
            print(
                f"Error: defaults table does not exist in the {table_name} table, check the configuration file"
            )
            raise SystemExit()

    def table_func_retrieve_additional_configs(self, table_name, func_name):

        table_entries = self.get_config_value(self.CONFIGURATION_FILE_NAME)
        try:
            tb_entries = self._get_toml_table_entrys(table_entries, table_name)
        except KeyError:
            print(
                f"Error: {table_name} table does not exist in the configuration file"
            )
            raise SystemExit()
        if func_name not in tb_entries:
            return type(table_entries)()
        elif (
            len(tb_entries[func_name]) == 0
        ):  # empty [func_name] ... [another_func_name] key: value
            return type(table_entries)()
        else:
            return tb_entries[func_name]

    def config_exist(self, config):

        return self.get_config_value(config) != self._EMPTY_CONFIG

    def get_config_value(self, config):

        # map(lambda pair: pair[0] ) # TODO MAGIC NUMBERS

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
