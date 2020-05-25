"""Serves as a factory for action objects.

Types of 'Action's exist in the 'actions' subpackage. These
actions are instantiated through this module.

"""
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
    """The way of creating action objects in pyrepoman.

    """

    @classmethod
    def create_action(cls, configholder):
        """Creates and returns a action object.

        Parameters
        --------
        configholder : ConfigHolder
            An instantiation of ConfigHolder, used to hold program configurations.

        Returns
        --------
        Action
            A subclass object of 'Action' should be returned.

        Raises
        --------
        toml.decoder.TomlDecodeError
            If the configuration file for the program has a
            syntax error when loaded.
        subprocess.CalledProcessError
            If the user chooses to communicate with
            a remotehost and the program fails to talk
            to the remotehost (see notes).
        SystemExit
            If invalid additional action/host argument(s) are
            passed in (see notes).
        KeyError
            If a webhost is unable to load 'default'
            configurations from the configuration file.
        PermissionError
            If the dot character (alone anyways) is passed as
            the localhost argument.

        Notes
        --------
        In regards to the 'subprocess.CalledProcessError'.
        When determining if a user has chosen a remotehost
        to retrieve Git repos from, two calls are made to the remotehost.
        Both calls are through the subprocess library.

        In regards to the 'SystemExit'.
        It is possible that a user can request a valid host but pass
        in a invalid argument (e.g. localhost with a path that does
        not exist on the system). This will result in cause the
        HostFactory to raise SystemExit. ActionFactory contains the
        same ability, however the current program implementation
        forbids users from entering in a invalid action.

        """
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
                return lambda: update.Update()
            elif fetch.Fetch.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return lambda: fetch.Fetch(host)
            elif archive.Archive.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return lambda: archive.Archive(host)
            elif backup.Backup.is_action_type(identifier):
                host = HostFactory.create_host(configholder)
                return lambda: backup.Backup(host)
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
