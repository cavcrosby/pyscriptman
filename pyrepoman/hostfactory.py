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
    @classmethod
    def create_host(cls, configholder):

        try:
            identifier = configholder.get_config_value(Host.HOST_CMD_ARG_NAME)
            host = cls._determine_host_type(identifier, configholder)
            return host()
        except toml.decoder.TomlDecodeError:
            raise
        except subprocess.CalledProcessError:
            raise
        except (SystemExit, KeyError, PermissionError):
            raise

    @classmethod
    def _determine_host_type(cls, identifier, configholder):

        if github.GitHub.is_host_type(identifier):
            return (lambda: cls._github_pre_post_construction(configholder))
        elif localhost.LocalHost.is_host_type(identifier, configholder):
            return (lambda: localhost.LocalHost(configholder))
        elif remotehost.RemoteHost.is_host_type(identifier, configholder):
            return (lambda: remotehost.RemoteHost(configholder))
        else:
            Message.print_generator_invalid_host(configholder)
            sys.exit(1)

    @classmethod
    def _github_pre_post_construction(cls, configholder):

        configholder.load_toml()
        host = github.GitHub(configholder)
        host.load_config_defaults()
        return host
