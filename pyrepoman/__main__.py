#!/usr/bin/env python3
# Standard Library Imports
from subprocess import CalledProcessError

# Third Party Imports
import requests
from toml import TomlDecodeError

# Local Application Imports
from pyrepoman.generator import Generator
from pyrepoman.cmd import Cmd
from util.configholder import ConfigHolder
from util.message import Message
from pyrepoman.pyrepoman_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)


def pyrepoman():

    try:
        configholder = ConfigHolder.from_object_dict(
            Cmd.retrieve_args(), CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH
        )
        action = Generator.generate_action(configholder)
        action.run()
    except (
        CalledProcessError,
        FileNotFoundError,
        PermissionError,
        SystemExit,
        TomlDecodeError,
        AttributeError,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
    ):
        pass
    except Exception as e:
        Message.print_unknown_error_occurred(e)


if __name__ == "__main__":
    pyrepoman()
