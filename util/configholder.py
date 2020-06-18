"""Class module for configholder."""
# Standard Library Imports

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message
from util.config import Config


class ConfigHolder:
    """How configurations are stored and accessed.

    Parameters
    ----------
    CONFIGURATION_FILE_NAME : str
        Name of configuration file.
    CONFIGURATION_FILE_PATH : str
        Path of configuration file.

    """

    @property
    def NON_EXISTANT_CONFIG(self):
        """How a config that does not exist is represented.
        
        Returns
        -------
        NoneType
            How nonexistant configs are represented.
        
        """
        return None

    @property
    def _DEFAULTS_ENTRY_NAME(self):
        """The table name that default configurations are stored under.
        
        Returns
        -------
        str
            The default table name that stores default configurations.
        
        """
        return "defaults"

    def __init__(self, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):

        self.configs = list()
        self.CONFIGURATION_FILE_NAME = CONFIGURATION_FILE_NAME
        self.CONFIGURATION_FILE_PATH = CONFIGURATION_FILE_PATH

    @classmethod
    def from_object_dict(cls, obj, CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH):
        """Additional constructor."""
        configholder = cls(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
        transformed_args = vars(obj)
        [
            configholder.add_config(arg, transformed_args[arg])
            for arg in transformed_args
        ]
        return configholder

    @staticmethod
    def _get_toml_table_entries(table, index):
        """How to get entries from a table (See Also).

        Parameters
        ----------
        table : dict of tables/key pairs
            A container for more tables and key pairs.
        index : str
            Table name to slice by.

        Returns
        -------
        dict
            Key pairs and/or tables will be returned.

        See Also
        --------
        https://github.com/toml-lang/toml
        
        """
        return table[index]

    def get_config(self, config_name):
        """How to retrieve a config object.
        
        Parameters
        ----------
        config_name : str
            Configuration name to search by.

        Returns
        -------
        util.config.Config
            A config object.
        NoneType
            This means no configuration existed with this configuration
            name.
        
        """
        for config in self.configs:
            if config.name == config_name:
                return config

        return self.NON_EXISTANT_CONFIG

    def add_config(self, config_name, value):
        """How to add a config object.
        
        Parameters
        ----------
        config_name : str
            Configuration name to search by.
        value : str or int
            The value of the configuration.

        Notes
        -----
        Warning is printed if a Config object with the same name
        exists in the configholder. This duplicate Config object will
        also be overwritten.
        
        """
        if self.config_exist(config_name):
            Message.print_configholder_duplicate_config_inserted(config_name, value)
            self.delete_config(config_name)
        self.configs.append(Config(config_name, value))

    def delete_config(self, config_name):
        """How to delete a config object from configholder.
        
        Parameters
        ----------
        config_name : str
            Configuration name to search by.
        
        """
        if not self.config_exist(config_name):
            Message.print_configuration_not_exist(config_name)
            raise KeyError
        config = self.get_config(config_name)
        self.configs.remove(config)

    def config_exist(self, config_name):
        """How to determine if a config exists in the configholder.
        
        Parameters
        ----------
        config_name : str
            Configuration name to search by.

        Returns
        -------
        bool
            Whether or not the Config object exists in the configholder.
        
        """
        return self.get_config(config_name) != self.NON_EXISTANT_CONFIG

    def get_config_value(self, config_name):
        """How to get a Config object's value.
        
        Parameters
        ----------
        config_name : str
            Configuration name to search by.

        Returns
        -------
        str
            One possible value type of the Config object.
        int
            Another possible value type of the Config object.
        NoneType
            Another possible value type of the Config object.

        """
        config = self.get_config(config_name)

        if config != self.NON_EXISTANT_CONFIG:
            return config.value

        return config

    def load_toml(self):
        """How toml files are added to configholder.

        Raises
        ------
        toml.decoder.TomlDecodeError
            If the configuration file loaded has a
            syntax error when loaded.

        """
        try:
            self.add_config(
                self.CONFIGURATION_FILE_NAME, toml.load(self.CONFIGURATION_FILE_PATH)
            )
        except PermissionError as e:
            Message.print_permission_denied(e.filename)
            raise
        except toml.decoder.TomlDecodeError as e:
            Message.print_toml_decodeerror(e)
            raise

    def retrieve_table_defaults(self, table_name):
        """How to retrieve configuration 'defaults' from a specfic table.

        Parameters
        ----------
        table_name : str
            Table name to search by.

        Returns
        -------
        dict
            Key pairs will be returned.

        Raises
        ------
        KeyError
            If the table requested does not exist or
            the 'default' table where default configurations
            are stored does not exist.

        """
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
            Message.print_default_table_does_notexist(
                self._DEFAULTS_ENTRY_NAME, table_name
            )
            raise

    def table_func_retrieve_additional_configs(self, table_name, func_name):
        """Getting additional configurations that are required by webhosts.

        Webhosts may have functions that require
        additional configurations. Hence they are
        only loaded if actual function runs.

        Parameters
        ----------
        table_name : str
            Table name to search by.
        func_name : str
            Function name to search by.

        Returns
        -------
        dict
            Either an empty dict (or table) will be
            returned or key pairs will be returned.

        Raises
        ------
        KeyError
            If the table requested does not exist.

        """
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
        ):  # empty is considered [func_name] () vs. [another_func_name] (key: value) ...
            return type(tables)()
        else:
            return table_entries[func_name]

    def __str__(self):
        """Returns values of Config objects selected in debug_configs_names.
        
        Returns
        -------
        str
            A dictionary that will be represented as a string.
            That will be of the Config object names and values.
        
        """
        debug_configs_names = ["path", "host", "host_path"]
        return str(
            {
                debug_configs_name: self.get_config_value(debug_configs_name)
                for debug_configs_name in debug_configs_names
                if self.get_config_value(debug_configs_name) != self.NON_EXISTANT_CONFIG
            }
        )
