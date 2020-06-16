"""The abstract class module for all web hosts.

A web host is defined as a website/web application
that hosts users' Git repos.

"""
# Standard Library Imports
from abc import abstractmethod
import inspect

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host


class WebHost(Host):
    """The abstract class for all web hosts.

    Web host subclasses are created under the assumption
    that their abstract methods are defined in class scope.
    This also includes any abstract methods and variables
    in the grandfather Host class (See Also).

    Parameters
    ----------
    configholder : util.configholder.ConfigHolder
        An instantiation of ConfigHolder, used to hold program configurations.
    
    Methods
    ----------
    get_user_repo_names_and_locations
        How function configurations are loaded when
        the function is called. Used to enforce consistent
        structure.

    See Also
    ----------
    pyrepoman.hosts.host
    pyrepoman.hosts.host.add_repo_name_and_location

    Notes
    ----------
    _get_user_repo_names_and_locations
        To be implemented, retrieves and stores
        bare Git repo names and locations (See Also).

    """

    def __init__(self, configholder):

        super().__init__()
        self.configholder = configholder

    def load_config_defaults(self):
        """How default configurations are loaded.

        Raises
        ----------
        KeyError
            If the webhost does not have a table in the
            configuration file or the 'default' table
            where default configurations are stored does not exist.

        """
        try:
            default_configs = self.configholder.retrieve_table_defaults(
                self._get_host_name()
            )
            for default_config in default_configs:
                setattr(self, default_config, default_configs[default_config])
        except KeyError:
            raise

    def get_user_repo_names_and_locations(self):
        """How additional configurations are loaded for the function.

        Raises
        ----------
        KeyError
            If the webhost does not have a table in the
            configuration file.

        """
        try:
            func_configs = self.configholder.table_func_retrieve_additional_configs(
                self._get_host_name(), inspect.currentframe().f_code.co_name
            )  # inspect.currentframe().f_code.co_name returns function name
            for func_config in func_configs:
                setattr(self, func_config, func_configs[func_config])
            return self._get_user_repo_names_and_locations()
        except KeyError:
            raise

    @abstractmethod
    def _get_user_repo_names_and_locations(self):
        """To be implemented.

        Retrieves and stores bare Git repo names and locations.

        """
        NotImplemented
