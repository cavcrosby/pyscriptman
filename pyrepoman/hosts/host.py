"""The abstract class module for all hosts."""
# Standard Library Imports
from abc import ABC, abstractmethod, abstractclassmethod

# Third Party Imports

# Local Application Imports
from util.helpers import get_typeof_repo_names
from util.message import Message


class Host(ABC):
    """The abstract class for all hosts.

    Host subclasses are created under the assumption
    that their abstract methods are defined and `HELP_DESC`
    is also defined in class scope (see __init_subclass__).
   
    Attributes
    ----------
    HELP_DESC : NotImplemented
        Parser description provided of a host
        when using -h/--help (See Also).
    HOST_KEY : str
        Chosen host is stored under this name.
    
    Methods
    ----------
    add_parser : subparser_container
        How hosts are added to the command line to be used.
        Used to enforce consistent structure.

    See Also
    ----------
    pyrepoman.LocalHost --> HELP_DESC Example
    pyrepoman.RemoteHost --> HELP_DESC Example
    pyrepoman.GitHub --> HELP_DESC Example
    
    Notes
    ----------
    _modify_parser : parser
        To be implemented, allows the host parser to
        take custom arguments.

    """

    HELP_DESC = NotImplemented
    HOST_KEY = "host"

    @property
    def repo_names_and_locations(self):
        """Getter for returning repo names and locations"""
        return self._repo_names_and_locations

    @property
    def repo_names(self):
        """Getter for repo names"""
        return self._repo_names_and_locations.keys()

    def __init__(self):

        self._repo_names_and_locations = dict()

    def __init_subclass__(cls, *args, **kwargs):
        """Specifications required by future host subclasses."""
        super().__init_subclass__(*args, **kwargs)

        if cls.HELP_DESC is NotImplemented and cls.__name__ != "WebHost":
            raise NotImplementedError(
                Message.construct_helpdesc_notimplemented_msg({cls.__name__})
            )

    @staticmethod
    def _get_bare_repo_names_from_path(dir_path):
        """Retrieve's bare Git repos from a given directory path.

        Parameters
        ----------
        dir_path : str
            A directory path.

        """
        return get_typeof_repo_names(dir_path, barerepo=True)

    @classmethod
    def add_parser(cls, subparser_container, help_desc):
        """How hosts are added to the command line.

        Parameters
        ----------
        subparser_container : argparse._SubParsersAction
            The 'container' that the host subparser is added to
            (see notes).

        Notes
        ----------
        It should be noted that subparser_container is
        technically not actually an container, but
        a 'special action object' (see argparser documentation).

        """
        subcommand = cls._get_host_name()
        parser = subparser_container.add_parser(
            subcommand, help=help_desc, allow_abbrev=False
        )
        parser = cls._modify_parser(parser)
        parser.set_defaults(**{cls.HOST_KEY: subcommand})
        return parser

    @classmethod
    def _get_host_name(cls):
        """How the host name is returned."""
        return cls.__name__.lower()

    def add_repo_name_and_location(self, repo_name, location):
        """How to add repo name and location to host's repos names and locations
        
        Parameters
        ----------
        repo_name : str
            The name of the Git repo to store.
        location : str
            A url to the Git repo.
        
        """
        self.repo_names_and_locations[repo_name] = location

    def get_location_from_repo_name(self, repo_name):
        """How to get the host's repo location from the repo name
        
        Parameters
        ----------
        repo_name : str
            The name of the Git repo to store.
        
        """
        return self.repo_names_and_locations[repo_name]

    @abstractclassmethod
    def is_host_type(cls, chosen_host, configholder):
        """How the host type is determined.

        Parameters
        ----------
        chosen_host : str
            Input received from the command line.
        configholder : util.configholder.ConfigHolder
            An instantiation of ConfigHolder, used to hold program configurations
            (see notes).

        Notes
        ----------
        The signature implemented in each host subclass
        does not have to be exact according to the base
        method and may not contain `configholder`.

        """
        NotImplemented

    @abstractclassmethod
    def _modify_parser(cls, parser):
        """To be implemented, allows the host parser to take custom arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        """
        NotImplemented

    @abstractmethod
    def get_user_repo_names_and_locations(self):
        """To be implemented.
        
        Depending on the type of host, this
        method is the 'how' in getting the repo names
        and locations.

        See Also
        ----------
        add_repo_name_and_location : For location definition

        """
        NotImplemented
