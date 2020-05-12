#!/usr/bin/env python3
# Standard Library Imports
from subprocess import CalledProcessError
import sys

# Third Party Imports
from toml import TomlDecodeError
from requests.exceptions import ConnectionError, HTTPError

# Local Application Imports
from pyrepoman.generator import Generator
from pyrepoman.cmd import Cmd
from util.printmessage import PrintMessage


def pyrepoman():

    try:
        configholder = Cmd.retrieve_args()
        action = Generator.generate_action(configholder)
        action.run()
    except (
        CalledProcessError,
        FileNotFoundError,
        PermissionError,
        SystemExit,
        TomlDecodeError,
        AttributeError,
        ConnectionError,
        HTTPError,
    ):
        pass
    except Exception as e:
        PrintMessage.print_unknown_error_occurred(e)


if __name__ == "__main__":
    pyrepoman()
