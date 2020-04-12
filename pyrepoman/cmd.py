# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports
from .configholder import ConfigHolder
from .actions import *

class Cmd():

    _DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(description=_DESC, prog='pyrepoman.py', allow_abbrev=False)

    @classmethod
    def retrieve_args(cls):
  
        _action_subparsers = cls._parser.add_subparsers(title='available actions', metavar='action [options ...]')
        _action_subparsers.required = True

        update.Update.add_parser(_action_subparsers, help_desc=update.Update.HELP_DESC)

        fetch.Fetch.add_parser(_action_subparsers, help_desc=fetch.Fetch.HELP_DESC)

        backup.Backup.add_parser(_action_subparsers, help_desc=backup.Backup.HELP_DESC)

        archive.Archive.add_parser(_action_subparsers, help_desc=archive.Archive.HELP_DESC)

        args = cls._parser.parse_args()

        return ConfigHolder(args)