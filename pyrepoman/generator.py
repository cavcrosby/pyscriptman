# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports
from .configholder import ConfigHolder
from .hosts.webhosts import *
from .hosts import *
from .actions import *

class Generator:

    _DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    _parser = argparse.ArgumentParser(description=_DESC, prog='pyrepoman.py', allow_abbrev=False)
    _require_subcommands = True

    @classmethod
    def generate_cmd_args(cls):

        host_title = 'available hosts'
        host_metavar = 'host [options ...]'
        
        _action_subparsers = cls._parser.add_subparsers(title='available actions', metavar='action [options ...]')
        _action_subparsers.required = cls._require_subcommands
        parser_update = update.Update.add_parser(_action_subparsers)

        parser_fetch = fetch.Fetch.add_parser(_action_subparsers)
        fetch_host_subparsers = parser_fetch.add_subparsers(title=host_title, metavar=host_metavar)
        fetch_host_subparsers.required = cls._require_subcommands
        github.GitHub.add_parser(fetch_host_subparsers)
        remotehost.RemoteHost.add_parser(fetch_host_subparsers)
        localhost.LocalHost.add_parser(fetch_host_subparsers)

        parser_backup = backup.Backup.add_parser(_action_subparsers)
        backup_host_subparsers = parser_backup.add_subparsers(title=host_title, metavar=host_metavar)
        backup_host_subparsers.required = cls._require_subcommands
        github.GitHub.add_parser(backup_host_subparsers)
        remotehost.RemoteHost.add_parser(backup_host_subparsers)
        localhost.LocalHost.add_parser(backup_host_subparsers)

        parser_archive = archive.Archive.add_parser(_action_subparsers)
        archive_host_subparsers = parser_archive.add_subparsers(title=host_title, metavar=host_metavar)
        archive_host_subparsers.required = cls._require_subcommands
        github.GitHub.add_parser(archive_host_subparsers)
        remotehost.RemoteHost.add_parser(archive_host_subparsers)
        localhost.LocalHost.add_parser(archive_host_subparsers)

        args = cls._parser.parse_args()

        return ConfigHolder(args)


    @classmethod
    def generate_action(cls, configholder):

        identifier = configholder.get_config_value('action')

        if(update.Update.is_action_type(identifier)):
            return update.Update()
        elif (fetch.Fetch.is_action_type(identifier)):
            host = cls._generate_host(configholder)
            return fetch.Fetch(host)
        elif (archive.Archive.is_action_type(identifier)):
            host = cls._generate_host(configholder)
            return archive.Archive(host, configholder)
        elif (backup.Backup.is_action_type(identifier)):
            host = cls._generate_host(configholder)
            return backup.Backup(host, configholder)
        else:
            print(f"Error: Invalid action target; action {configholder.get_config_value('action')}")
            raise SystemExit()

    @classmethod
    def _generate_host(cls, configholder):

        identifier = configholder.get_config_value('host')

        if(github.GitHub.is_host_type(identifier, configholder)):
            configholder.load_toml()
            github_host = github.GitHub(configholder)
            github_host.load_config_defaults() # TODO, TEST THIS PART OF THE CODE BY GIVING WACKY (BUT VALID) CONFIGS IN CONFIG FILE
            return github_host
        elif(localhost.LocalHost.is_host_type(identifier, configholder)):
            return localhost.LocalHost(configholder)
        elif(remotehost.RemoteHost.is_host_type(identifier, configholder)):
            return remotehost.RemoteHost(configholder)
        else:
            configs = ['path', 'host', 'host_path']
            error_string = 'Error: Invalid host target;'
            for config in configs:
                config_value = configholder.get_config_value(config)
                if(config_value != configholder.EMPTY_CONFIG):
                    error_string += f" {config} {config_value};"
            print(error_string)
            raise SystemExit()
