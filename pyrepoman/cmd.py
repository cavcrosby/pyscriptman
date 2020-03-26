# Standard Library Imports
import argparse, sys

# Third Party Imports

# Local Application Imports
from .configholder import ConfigHolder

class Cmd():

    _DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(description=_DESC, prog="pyrepoman.py", allow_abbrev=False)
    _action_subparsers = _parser.add_subparsers(title="available actions", metavar="action [options ...]")

    @staticmethod
    def action_only_passed(namespace, action_name, num_args):

        if(namespace.action == action_name and len(sys.argv) == num_args):
            return True

        return False

    @staticmethod
    def _add_github(subparser_container):

        REPO_TYPES = ['all', 'public', 'private']

        parser_github = subparser_container.add_parser('github', help='a popular web hosting for git repos', allow_abbrev=False)
        parser_github.add_argument('--repo-type', metavar="TYPE", default='all', choices=REPO_TYPES, help='specifies the type of repos to work on, choices are (default: all): ' + ', '.join(REPO_TYPES))
        parser_github.set_defaults(host='github')

    @staticmethod
    def _add_localhost(subparser_container):

        parser_localhost = subparser_container.add_parser('localhost', help='can manipulate directories containing git repos', allow_abbrev=False)
        parser_localhost.add_argument('path', help='specifies what directory you wish to target')
        parser_localhost.set_defaults(host='path')

    @staticmethod
    def _add_remotehost(subparser_container):

        DEFAULT_HOST_PATH = '$HOME'

        parser_remotehost = subparser_container.add_parser('remotehost', help='can target directories on remote hosts', allow_abbrev=False)
        parser_remotehost.add_argument('host', help='specifies what host you wish to target, host format is the format of hostname in ssh')
        parser_remotehost.add_argument('--host-path', metavar="path", default=DEFAULT_HOST_PATH, help=f'specifies what directory on the host to target for repos (default: {DEFAULT_HOST_PATH}).')

    @classmethod
    def retrieve_args(cls):

        cls._add_update()
        parser_fetch = cls._add_fetch()
        parser_archive = cls._add_archive()
        parser_backup = cls._add_backup()

        if(len(sys.argv) == 1): # just the program name was passed
            cls._parser.print_usage()
            sys.exit(1)

        args = cls._parser.parse_args()
        if(cls.action_only_passed(args, 'fetch', 2)):
            parser_fetch.print_usage()
            sys.exit(1)
        if(cls.action_only_passed(args, 'archive', 3)):
            parser_archive.print_usage()
            sys.exit(1)
        if(cls.action_only_passed(args, 'backup', 3)):
            parser_backup.print_usage()
            sys.exit(1)

        return ConfigHolder(args)

    @classmethod
    def _add_update(cls):

        parser_update = cls._action_subparsers.add_parser('update', help='update all Git repos in your current directory from remote repos')
        parser_update.set_defaults(action='update')
        parser_update.set_defaults(host='')
    
    @classmethod
    def _add_fetch(cls):

        parser_fetch = cls._action_subparsers.add_parser('fetch', help='fetch all Git repos through a web provider', allow_abbrev=False)
        host_subparsers = parser_fetch.add_subparsers(title="available hosts", metavar="host [options ...]")
        cls._add_github(host_subparsers)
        cls._add_localhost(host_subparsers)
        cls._add_remotehost(host_subparsers)
        parser_fetch.set_defaults(action='fetch')
        return parser_fetch

    @classmethod
    def _add_archive(cls):

        parser_archive = cls._action_subparsers.add_parser('archive', help='archive all Git repos, done by bundling repos', allow_abbrev=False)
        parser_archive.add_argument('dest', help='where to store archives (destination)')
        host_subparsers = parser_archive.add_subparsers(title="available hosts", metavar="host [options ...]")
        cls._add_github(host_subparsers)
        cls._add_localhost(host_subparsers)
        cls._add_remotehost(host_subparsers)
        parser_archive.set_defaults(action='archive')
        return parser_archive

    @classmethod
    def _add_backup(cls):

        parser_backup = cls._action_subparsers.add_parser('backup', help='backup all Git repos, done by mirroring repos fully', allow_abbrev=False)
        parser_backup.add_argument('dest', help='where to store backups (destination)')
        host_subparsers = parser_backup.add_subparsers(title="available hosts", metavar="host [options ...]")
        cls._add_github(host_subparsers)
        cls._add_localhost(host_subparsers)
        cls._add_remotehost(host_subparsers)
        parser_backup.set_defaults(action='backup')
        return parser_backup

    @classmethod
    def _strlower(cls, s):

        return s.lower()

try:
    c = Cmd()
    print(c.retrieve_args())
except SystemExit:
    pass
