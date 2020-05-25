"""Serves as a factory for host objects.

Types of 'Host's exist in the 'hosts' subpackage. These
hosts are instantiated through this module.

"""
# Standard Library Imports
import sys
import subprocess

# Third Party Imports
import toml

# Local Application Imports
from pyrepoman.hosts import localhost, remotehost
from pyrepoman.hosts.webhosts import github
from pyrepoman.hosts.host import Host
from util.message import Message


class HostFactory:
    """The way of creating host objects in pyrepoman.

    """
    @staticmethod
    def _return_localhost_constructor(configholder):
        """Returns 'LocalHost' class wrapped in lambda to fufill parameters.

        """
        return lambda: localhost.LocalHost(configholder)

    @staticmethod
    def _return_remotehost_constructor(configholder):
        """Returns 'RemoteHost' class wrapped in lambda to fufill parameters.

        """
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
        --------
        configholder : ConfigHolder
            An instantiation of ConfigHolder, used to hold program configurations.

        Returns
        --------
        Host
            A instantiation of a 'host' subclass should be returned.

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
            If invalid additional host argument(s) are
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
        HostFactory to raise SystemExit.

        """
        try:
            host_name = configholder.get_config_value(Host.HOST_CMD_ARG_NAME)
            host_constructor = cls._get_host_constructor(host_name, configholder)
            return host_constructor()
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise

    @classmethod
    def _get_host_constructor(cls, host_name, configholder):
        """Finds correct host constructor then returns an 'Host' subclass.

        Parameters
        --------
        host_name : str
            This is the host chosen by the user from the command line.
        configholder : ConfigHolder
            An instantiation of ConfigHolder, used to hold program configurations.

        Returns
        --------
        Host
            A subclass of 'Host' should be returned.

        Raises
        --------
        (see create_host 'Raises' section.)

        """
        if github.GitHub.is_host_type(host_name):
            return cls._return_github_constructor(configholder)
        elif localhost.LocalHost.is_host_type(host_name, configholder):
            return cls._return_localhost_constructor(configholder)
        elif remotehost.RemoteHost.is_host_type(host_name, configholder):
            return cls._return_remotehost_constructor(configholder)
        else:
            Message.print_generator_invalid_host(configholder)
            sys.exit(1)
