# Standard Library Imports
from abc import ABC, abstractclassmethod
import os, subprocess, shutil, re, sys

# Third Party Imports

# Local Application Imports
from util.helpers import get_typeof_repo_names_no_path
from util.message import Message


class Action(ABC):

    HELP_DESC = NotImplemented  # this class var should be implemented in subclasses
    ACTION_CMD_ARG_NAME = "action"

    _HOST_SUBPARSER_TITLE = "[available hosts]"
    _HOST_SUBPARSER_METAVAR = "host [options ...]"
    _REQUIRE_SUBCOMMANDS = True

    def __init_subclass__(cls, *args, **kwargs):

        super().__init_subclass__(*args, **kwargs)

        if cls.HELP_DESC is NotImplemented:
            raise NotImplementedError(
                Message.construct_helpdesc_notimplemented_msg({cls.__name__})
            )

    @staticmethod
    def _get_pwd_local_nonbare_repo_names():

        return get_typeof_repo_names_no_path(os.getcwd(), False)

    @classmethod
    def is_action_type(cls, chosen_action):

        return chosen_action == cls._get_action_name()

    @classmethod
    def _get_action_name(cls):

        return cls.__name__.lower()

    @classmethod
    def add_parser(cls, subparser_container, help_desc):

        subcommand = cls._get_action_name()
        parser = subparser_container.add_parser(
            subcommand, help=cls.HELP_DESC, allow_abbrev=False
        )
        parser = cls._modify_parser(parser)
        parser.set_defaults(**{cls.ACTION_CMD_ARG_NAME: subcommand})
        return parser

    @abstractclassmethod
    def _modify_parser(cls, parser):

        pass

    @abstractclassmethod
    def run(cls):

        """ HOW EACH ACTION IS TO PERFORM ITS FUNCTIONALITY """

        pass
