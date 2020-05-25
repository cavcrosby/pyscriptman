"""How pyrepoman interfaces with the command line.

"""
# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports
from pyrepoman.actions import update, fetch, backup, archive


class Cmd:
    """How pyrepoman interfaces with the command line.

    Attributes
    ----------
    _DESC : str
            Command line program description printed when --help/-h
            is given with just the executable name.
    _parser : ArgumentParser
            This is the root parser for the program.

    """
    _DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(
        description=_DESC, prog="pyrepoman.py", allow_abbrev=False
    )

    @classmethod
    def retrieve_args(cls):
        """How arguments are retrieved from the command line.

        Returns
        --------
        Namespace
            An object that holds attributes pulled from the command line.

        Raises
        --------
        SystemExit
            If user input is not considered valid when parsing args

        """
        _action_subparsers = cls._parser.add_subparsers(
            title="available actions", metavar="action [options ...]"
        )
        _action_subparsers.required = True

        update.Update.add_parser(_action_subparsers, help_desc=update.Update.HELP_DESC)

        fetch.Fetch.add_parser(_action_subparsers, help_desc=fetch.Fetch.HELP_DESC)

        backup.Backup.add_parser(_action_subparsers, help_desc=backup.Backup.HELP_DESC)

        archive.Archive.add_parser(
            _action_subparsers, help_desc=archive.Archive.HELP_DESC
        )

        args = cls._parser.parse_args()

        return args
