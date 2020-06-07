"""The abstract class module for all actions."""
# Standard Library Imports
import os
from abc import ABC, abstractclassmethod

# Third Party Imports

# Local Application Imports
from util.helpers import get_typeof_repo_names
from util.message import Message


class Action(ABC):
    """The abstract class for all actions.

    Action subclasses are created under the assumption
    that their abstract methods are defined and `HELP_DESC`
    is also defined in class scope (see __init_subclass__).
   
    Attributes
    ----------
    _HOST_SUBPARSERS_TITLE : str
        Title for selection of hosts.
    _HOST_SUBPARSER_METAVAR : str
        Action's host argument name.
    HELP_DESC : NotImplemented
        Description provided for an action when using
        -h/--help with no action provided.
    ACTION_CMD_ARG_NAME : str
        Chosen action is stored under this name.
    
    Methods
    ----------
    add_parser : subparser_container
        How actions are added to the command line to be used.
        Used to enforce consistent structure.
    run
        To be implemented, what you want the action to do.
    
    Notes
    ----------
    _modify_parser : parser
        To be implemented, allows the action parser to
        take custom arguments.

    """
    _HOST_SUBPARSERS_TITLE = "available hosts"
    _HOST_SUBPARSER_METAVAR = "host [options ...]"

    HELP_DESC = NotImplemented
    ACTION_CMD_ARG_NAME = "action"

    def __init_subclass__(cls, *args, **kwargs):
        """Specifications required by future action subclasses."""
        super().__init_subclass__(*args, **kwargs)

        if cls.HELP_DESC is NotImplemented:
            raise NotImplementedError(
                Message.construct_helpdesc_notimplemented_msg({cls.__name__})
            )

    @staticmethod
    def _get_pwd_local_nonbare_repo_names():
        """Returns bare repos in the current present working directory.
        
        Returns
        --------
        list of str(s)
            A list of git repo name(s).
        
        """
        return get_typeof_repo_names(os.getcwd(), barerepo=False)

    @classmethod
    def _get_action_name(cls):
        """How the action name is returned.
        
        Returns
        --------
        str
            A lower case action name.
        
        """
        return cls.__name__.lower()

    @classmethod
    def is_action_type(cls, chosen_action):
        """How the action type is determined.

        Parameters
        ----------
        chosen_action : str
            Input received from the command line.

        Returns
        --------
        bool
            Whether the action was chosen or not.

        """
        return chosen_action == cls._get_action_name()

    @classmethod
    def add_parser(cls, subparser_container):
        """How actions are added to the command line.

        Parameters
        ----------
        subparser_container : argparse._SubParsersAction
            The 'container' that the action subparser is added to
            (see notes).

        Returns
        --------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        Notes
        ----------
        It should be noted that subparser_container is
        technically not actually an container, but
        a 'special action object' (see argparser documentation).

        """
        subcommand = cls._get_action_name()
        parser = subparser_container.add_parser(
            subcommand, help=cls.HELP_DESC, allow_abbrev=False
        )
        parser = cls._modify_parser(parser)
        parser.set_defaults(**{cls.ACTION_CMD_ARG_NAME: subcommand})
        return parser

    @abstractclassmethod
    def _modify_parser(cls, parser):
        """To be implemented, allows the action parser to take custom arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        """
        NotImplemented

    @abstractclassmethod
    def run(cls):
        """To be implemented, what you want the action to do."""
        NotImplemented
