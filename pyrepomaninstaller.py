#!/usr/bin/env python3

"""This is the main entry for pyrepoman."""
# Standard Library Imports
import platform
import os
import pathlib
from os.path import join

# Third Party Imports

# Local Application Imports
from util.message import Message
from global_variables import ROOTDIR, EXECUTABLE_LOCATION


class PyrepomanInstaller:

    SUPPORTED_OSES = ["linux"]
    LINK_NAME = "pyrepoman"

    def __init__(self):

        self.os_name = platform.system().lower()
        self.system_python_path = os.getenv("PYTHONPATH")
        self.user_bin_path = os.path.expanduser("~/bin")
        self.user_bin_exist = pathlib.Path(self.user_bin_path).exists()
        self.link_path = join(self.user_bin_path, self.LINK_NAME)
        self.installed = (
            True
            if (
                pathlib.Path(EXECUTABLE_LOCATION).exists()
                and pathlib.Path(self.link_path).exists()
            )
            else False
        )

    def install(self):

        if self.os_name not in self.SUPPORTED_OSES:
            Message.print_non_supported_os(self.os_name)
        else:
            if not self.user_bin_exist:
                os.mkdir(self.user_bin_path)
            os.symlink(EXECUTABLE_LOCATION, self.link_path)
            # TODO WORK ON GETTING LIBRARY/PACKAGE INTO BASHRC FILE(S)


if __name__ == "__main__":
    installer = PyrepomanInstaller()
    installer.install()
