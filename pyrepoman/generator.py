# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .hosts.webhosts import *
from .hosts import *
from .actions import *
from .exceptions.hostgeneratorerror import HostGeneratorError
from .exceptions.actiongeneratorerror import ActionGeneratorError

class Generator:

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
            raise ActionGeneratorError(f"ActionGeneratorError: Invalid action target; action {configholder.get_config_value('action')}", configholder)

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
            error_string = 'HostGeneratorError: Invalid host target;'
            for config in configs:
                config_value = configholder.get_config_value(config)
                if(config_value != configholder.EMPTY_CONFIG):
                    error_string += f" {config} {config_value};"
            raise HostGeneratorError(error_string, configholder)   
    