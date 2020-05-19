# Standard Library Imports
import sys

# Third Party Imports

# Local Application Imports
from pyrepoman.actions.action import Action
from pyrepoman.hosts.host import Host
from pyrepoman.hosts.webhosts import *
from pyrepoman.hosts import *
from pyrepoman.actions import *
from util.message import Message


class Generator:
    @classmethod
    def generate_action(cls, configholder):

        identifier = configholder.get_config_value(Action.ACTION_CMD_ARG_NAME)

        if update.Update.is_action_type(identifier):
            return update.Update()
        elif fetch.Fetch.is_action_type(identifier):
            host = cls._generate_host(configholder)
            return fetch.Fetch(host)
        elif archive.Archive.is_action_type(identifier):
            host = cls._generate_host(configholder)
            return archive.Archive(host)
        elif backup.Backup.is_action_type(identifier):
            host = cls._generate_host(configholder)
            return backup.Backup(host)
        else:
            Message.print_generator_invalid_action(
                configholder.get_config_value(Action.ACTION_CMD_ARG_NAME)
            )
            sys.exit(1)

    @classmethod
    def _generate_host(cls, configholder):

        identifier = configholder.get_config_value(Host.HOST_CMD_ARG_NAME)

        if github.GitHub.is_host_type(identifier):
            configholder.load_toml()
            github_host = github.GitHub(configholder)
            github_host.load_config_defaults()
            return github_host
        elif localhost.LocalHost.is_host_type(identifier, configholder):
            return localhost.LocalHost(configholder)
        elif remotehost.RemoteHost.is_host_type(identifier, configholder):
            return remotehost.RemoteHost(configholder)
        else:
            Message.print_generator_invalid_host(configholder)
            sys.exit(1)
