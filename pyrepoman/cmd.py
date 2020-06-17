"""How pyrepoman interfaces with the command line.

"""
# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports
from pyrepoman.pyrepoman_variables import REQUIRE_SUBCOMMANDS
from pyrepoman.actions import (
    update,
    fetch,
    backup,
    archive,
)


class Cmd:
    """How pyrepoman interfaces with the command line.

    Attributes
    ----------
    _DESC : str
        Command line program description printed when --help/-h
        is given with no other arguments/flags.
    _parser : ArgumentParser
        This is the root parser for command line arguments.

    """

    _DESC = """Description: This python application helps /
               manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(
        description=_DESC, prog="pyrepoman.py", allow_abbrev=False
    )

    @classmethod
    def retrieve_args(cls):
        """How arguments are retrieved from the command line.

        Returns
        -------
        Namespace
            An object that holds attributes pulled from the command line.

        Raises
        ------
        SystemExit
            If user input is not considered valid when parsing arguments.

        """
        _action_subparsers = cls._parser.add_subparsers(
            title="available actions", metavar="action [options ...]"
        )
        _action_subparsers.required = REQUIRE_SUBCOMMANDS

        update.Update.add_parser(_action_subparsers)

        fetch.Fetch.add_parser(_action_subparsers)

        backup.Backup.add_parser(_action_subparsers)

        archive.Archive.add_parser(_action_subparsers)

        # choosing an invalid action SHOULD NOT be possible.

        args = cls._parser.parse_args()

        return args
