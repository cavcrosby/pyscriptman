#!/usr/bin/env python3

"""This is the main entry for pyrepoman."""
# Standard Library Imports
import subprocess

# Third Party Imports
import requests
import toml

# Local Application Imports
from pyrepoman.actionfactory import ActionFactory
from pyrepoman.cmd import Cmd
from util.configholder import ConfigHolder
from util.message import Message
from pyrepoman.pyrepoman_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)


def pyrepoman():
    """The main of the pyrepoman program."""
    try:
        configholder = ConfigHolder.from_object_dict(
            Cmd.retrieve_args(),
            CONFIGURATION_FILE_NAME,
            CONFIGURATION_FILE_PATH
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
    pyrepoman()
