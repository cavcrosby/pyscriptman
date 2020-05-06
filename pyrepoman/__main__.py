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
        print("Error: an unknown error occured, please report the following below:")
        print(e)


if __name__ == "__main__":
    pyrepoman()
