# Standard Library Imports
import argparse, sys

# Third Party Imports

# Local Application Imports
from .configholder import ConfigHolder

# TODO, USE EACH CREATED SUBPARSER (ADD_PARSER) TO CREATE ANOTHER SUBPARSER GROUP (e.g. container = parser_fetch.add_subparsers(); container.add_parser())

class Cmd():

    _DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(description=_DESC, prog="pyrepoman.py", allow_abbrev=False)
    _subparsers = _parser.add_subparsers(title="available commands", metavar="command [options ...]")

    @classmethod
    def retrieve_args(cls):

        cls._add_update()
        cls._add_fetch()
        cls._add_backup()
        cls._add_archive()

        if(len(sys.argv) == 1): # just the program name was passed
            cls._parser.print_usage()
            sys.exit(1)

        return ConfigHolder(cls._parser.parse_args())

    @classmethod
    def _add_update(cls):

        parser_update = cls._subparsers.add_parser('update', help='update all Git repos in your current directory from remote repos')
        parser_update.set_defaults(action='update')
        parser_update.set_defaults(host='')
    
    @classmethod
    def _add_fetch(cls):

        parser_fetch = cls._subparsers.add_parser('fetch', help='fetch all Git repos through a web provider', allow_abbrev=False)
        group_fetch = parser_fetch.add_mutually_exclusive_group()
        parser_fetch.add_argument('host', help='specifies what host to target', type=cls._strlower)
        group_fetch.add_argument('--host-path', metavar="path", default="~/", help='specifies what directory on the host to target for repos')
        group_fetch.add_argument('--webhost', action="store_true", help='must be specified when using a web based Git hosting service (e.g GitHub)')
        group_fetch.add_argument('--local', action="store_true", help='must be specified when referring to a local directory')
        parser_fetch.set_defaults(action='fetch')

    @classmethod
    def _add_archive(cls):

        parser_archive = cls._subparsers.add_parser('archive', help='archive all Git repos, done by bundling repos', allow_abbrev=False)
        group_archive = parser_archive.add_mutually_exclusive_group()
        parser_archive.add_argument('host', help='specifies what host to target', type=cls._strlower)
        parser_archive.add_argument('archive_dir', help='what are you wanting to call the archive directory')
        group_archive.add_argument('--host-path', metavar="path", default="~/", help='specifies what directory on the host to target for repos')
        group_archive.add_argument('--webhost', action="store_true", help='must be specified when using a web based Git hosting service (e.g GitHub)')
        group_archive.add_argument('--local', action="store_true", help='must be specified when referring to a local directory')
        parser_archive.set_defaults(action='archive')

    @classmethod
    def _add_backup(cls):

        parser_backup = cls._subparsers.add_parser('backup', help='backup all Git repos, done by mirroring repos fully', allow_abbrev=False)
        group_backup = parser_backup.add_mutually_exclusive_group()
        parser_backup.add_argument('host', help='specifies what host to target', type=cls._strlower)
        parser_backup.add_argument('backup_dir', help='what are you wanting to call the backup directory')
        group_backup.add_argument('--host-path', metavar="path", default="~/", help='specifies what directory on the host to target for repos')
        group_backup.add_argument('--webhost', action="store_true", help='must be specified when using a web based Git hosting service (e.g GitHub)')
        group_backup.add_argument('--local', action="store_true", help='must be specified when referring to a local directory')
        parser_backup.set_defaults(action='backup')

    @classmethod
    def _strlower(cls, s):

        return s.lower()
