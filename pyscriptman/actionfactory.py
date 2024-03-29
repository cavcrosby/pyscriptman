"""Serves as a factory for action objects.

Types of "'Action's" exist in the 'actions' subpackage. These
actions are instantiated through this module.

"""
# Standard Library Imports
import sys
import subprocess

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message
from pyscriptman.hostfactory import HostFactory
from pyscriptman.actions.action import Action
from pyscriptman.actions import (
    update,
    fetch,
    backup,
    archive,
)


class ActionFactory:
    """The way of creating action objects in pyscriptman."""

    @staticmethod
    def _return_update_constructor():
        """Returns 'Update' class."""
        return update.Update

    @staticmethod
    def _return_fetch_constructor(host):
        """Returns 'Fetch' class wrapped in lambda."""
        return lambda: fetch.Fetch(host)

    @staticmethod
    def _return_backup_constructor(host):
        """Returns 'Backup' class wrapped in lambda."""
        return lambda: backup.Backup(host)

    @staticmethod
    def _return_archive_constructor(host):
        """Returns 'Archive' class wrapped in lambda."""
        return lambda: archive.Archive(host)

    @classmethod
    def create_action(cls, configholder):
        """Creates and returns a action object.

        Parameters
        ----------
        configholder : util.configholder.ConfigHolder
            An instantiation of ConfigHolder, used to hold program
            configurations.

        Returns
        -------
        Action
            An instantiated 'Action' subclass.

        Raises
        ------
        toml.decoder.TomlDecodeError
            If the configuration file loaded has a
            syntax error when loaded.
        subprocess.CalledProcessError
            If the user chooses to communicate with
            a remotehost and the program fails to
            have initial communcations to the remotehost.
        SystemExit
            If invalid additional action/host argument(s) are
            passed in (see notes).
        KeyError
            If a webhost is unable to load 'default'
            configurations from the configuration file.
        PermissionError
            If the present working directory has insufficient permissions
            and the dot character (alone anyways) is passed as
            the localhost argument.

        See Also
        --------
        pyscriptman.hostfactory

        Notes
        -----
        In regards to the 'SystemExit'. An example of this
        would be when a user chooses to pull repos from a localhost
        with a path that does not exist on the system (see Examples).

        Examples
        --------
        (pyscriptman) reap2sow1@Ron:~$ pyscriptman fetch localhost /foo/thispathdoesnotexist
        Error: Invalid host target; Configs passed in: {'path': '/foo/thispathdoesnotexist', 'host': 'localhost'}

        """
        try:
            action_name = configholder.get_config_value(
                Action.ACTION_CMD_ARG_NAME
            )
            action_constructor = cls._get_action_constructor(
                action_name, configholder
            )
            return action_constructor()
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise

    @classmethod
    def _get_action_constructor(cls, action_name, configholder):
        """Finds correct action type then returns an 'Action' subclass constructor.

        Parameters
        ----------
        action_name : str
            This is the action chosen by the user from the command line.
        configholder : ConfigHolder
            An instantiation of ConfigHolder, used to hold program
            configurations.

        Returns
        -------
        Action
            A subclass constructor of 'Action' should be returned.

        Raises
        ------
        (see create_action 'Raises' section.)

        """
        try:
            if update.Update.is_action_type(action_name):
                return cls._return_update_constructor()
            if fetch.Fetch.is_action_type(action_name):
                host = HostFactory.create_host(configholder)
                return cls._return_fetch_constructor(host)
            if archive.Archive.is_action_type(action_name):
                host = HostFactory.create_host(configholder)
                return cls._return_archive_constructor(host)
            if backup.Backup.is_action_type(action_name):
                host = HostFactory.create_host(configholder)
                return cls._return_backup_constructor(host)
            Message.print_factory_invalid_action(
                configholder.get_config_value(Action.ACTION_CMD_ARG_NAME)
            )
            sys.exit(1)
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise
