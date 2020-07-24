"""Serves as a factory for host objects.

Types of "'Host's" exist in the 'hosts' subpackage. These
hosts are instantiated through this module.

"""
# Standard Library Imports
import sys
import subprocess

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message
from pyscriptman.hosts.webhosts import github
from pyscriptman.hosts.host import Host
from pyscriptman.hosts import (
    localhost,
    remotehost,
)


class HostFactory:
    """The way of creating host objects in pyscriptman."""

    @staticmethod
    def _return_localhost_constructor(configholder):
        """Returns 'LocalHost' class wrapped in lambda."""
        return lambda: localhost.LocalHost(configholder)

    @staticmethod
    def _return_remotehost_constructor(configholder):
        """Returns 'RemoteHost' class wrapped in lambda."""
        return lambda: remotehost.RemoteHost(configholder)

    @staticmethod
    def _return_github_constructor(configholder):
        """Returns 'GitHub' object wrapped in lambda.

        In brief, webhosts may require additional configurations.
        Hence they may load the configuration file and their particular
        configurations.

        """
        configholder.load_toml()
        host = github.GitHub(configholder)
        host.load_config_defaults()
        return lambda: host

    @classmethod
    def create_host(cls, configholder):
        """Creates and returns a host object.

        Parameters
        ----------
        configholder : util.configholder.ConfigHolder
            An instantiation of ConfigHolder, used to hold program
            configurations.

        Returns
        -------
        Host
            An instantiated 'Host' subclass.

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
            If invalid additional host argument(s) are
            passed in (see notes).
        KeyError
            If a webhost is unable to load 'default'
            configurations from the configuration file.
        PermissionError
            If the present working directory has insufficient permissions
            and the dot character (alone anyways) is passed as
            the localhost argument.

        Notes
        -----
        In regards to the 'SystemExit'. An example of this
        would be when a user chooses to pull repos from a localhost
        with a path that does not exist on the system.

        """
        try:
            host_name = configholder.get_config_value(Host.HOST_KEY)
            host_constructor = cls._get_host_constructor(
                host_name, configholder
            )
            return host_constructor()
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise

    @classmethod
    def _get_host_constructor(cls, host_name, configholder):
        """Finds correct host type then returns an 'Host' subclass constructor.

        Parameters
        ----------
        host_name : str
            This is the host chosen by the user from the command line.
        configholder : util.configholder.ConfigHolder
            An instantiation of ConfigHolder, used to hold program
            configurations.

        Returns
        -------
        Host
            A subclass constructor of 'Host' should be returned.

        Raises
        ------
        (see create_host 'Raises' section.)

        """
        if github.GitHub.is_host_type(host_name):
            return cls._return_github_constructor(configholder)
        if localhost.LocalHost.is_host_type(host_name, configholder):
            return cls._return_localhost_constructor(configholder)
        if remotehost.RemoteHost.is_host_type(host_name, configholder):
            return cls._return_remotehost_constructor(configholder)
        Message.print_factory_invalid_host(configholder)
        sys.exit(1)
