# Standard Library Imports
import sys
import subprocess

# Third Party Imports
import toml

# Local Application Imports
from pyrepoman.actions import update, fetch, backup, archive
from pyrepoman.actions.action import Action
from util.message import Message
from pyrepoman.hostfactory import HostFactory


class ActionFactory:
    @classmethod
    def create_action(cls, configholder):

        try:
            identifier = configholder.get_config_value(Action.ACTION_CMD_ARG_NAME)
            action = cls._determine_action_type(identifier, configholder)
            return action()
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise

    @classmethod
    def _determine_action_type(cls, identifier, configholder):

        try:
            if update.Update.is_action_type(identifier):
                return (lambda: update.Update())
            elif fetch.Fetch.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return (lambda: fetch.Fetch(host))
            elif archive.Archive.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return (lambda: archive.Archive(host))
            elif backup.Backup.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return (lambda: backup.Backup(host))
            else:
                Message.print_generator_invalid_action(
                    configholder.get_config_value(Action.ACTION_CMD_ARG_NAME)
                )
                sys.exit(1)
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise