# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .hosts import *
from .actions import *

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
            return archive.Archive(host)
        elif (backup.Backup.is_action_type(identifier)):
            host = cls._generate_host(configholder)
            return backup.Backup(host)
        else:
            #TODO CREATE CUSTOM EXCEPTION
            raise GeneratorError(f"Error: No action called {identifier}")

    @classmethod
    def _generate_host(cls, configholder):

        identifier = configholder.get_config_value('host')

        if(github.GitHub.is_host_type(identifier, configholder)):
            github.GitHub.load_config_defaults(configholder)
            return github.GitHub(configholder)
        elif(localhost.LocalHost.is_host_type(identifier, configholder)):
            return localhost.LocalHost(configholder)
        elif(lanserver.LanServer.is_host_type(identifier, configholder)):
            return lanserver.LanServer(configholder)
        else:
            #TODO CREATE CUSTOM EXCEPTION
            raise GeneratorError(f"Error: Host, {identifier} is not supported")
