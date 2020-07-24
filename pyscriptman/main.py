#!/usr/bin/env python3

"""This is the main entry for pyscriptman."""
# Standard Library Imports
import subprocess

# Third Party Imports
import requests
import toml

# Local Application Imports
from pyscriptman.actionfactory import ActionFactory
from pyscriptman.cmd import Cmd
from util.configholder import ConfigHolder
from util.message import Message
from pyscriptman.pyscriptman_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)


def pyscriptman():
    """The main of the pyscriptman program."""
    try:
        configholder = ConfigHolder.from_object_dict(
            Cmd.retrieve_args(),
            CONFIGURATION_FILE_NAME,
            CONFIGURATION_FILE_PATH,
        )
        action = ActionFactory.create_action(configholder)
        action.run()
    except (
        FileNotFoundError,
        PermissionError,
        SystemExit,
        AttributeError,
        toml.TomlDecodeError,
        subprocess.CalledProcessError,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
    ):
        pass
    except Exception as e:
        Message.print_unknown_error_occurred(e)


if __name__ == "__main__":
    pyscriptman()
