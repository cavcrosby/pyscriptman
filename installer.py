#!/usr/bin/env python3

"""This is installer manager for pyscriptman."""
# Standard Library Imports
import platform
import os
import pathlib
import argparse
from os.path import join

# Third Party Imports

# Local Application Imports

ERROR_PREFIX = "Error:"
PROGRAM_NAME = "pyscriptman"
ROOTDIR = os.path.dirname(os.path.abspath(__file__))
EXECUTABLE_LOCATION = os.path.join(ROOTDIR, "pyscriptman/main.py")


class Installer:

    _DESC = f"""Description: Installer manager for {PROGRAM_NAME}."""
    _parser = argparse.ArgumentParser(description=_DESC, allow_abbrev=False)

    SUPPORTED_OSES = ["linux"]
    LOGIN_SHELL_CONFIG_FILES = [".bash_profile", ".bash_login", ".profile"]
    NONLOGIN_SHELL_CONFIG_FILES = [".bashrc"]
    DEFAULT_LOGIN_SHELL_CONFIG_FILE = LOGIN_SHELL_CONFIG_FILES[2]
    DEFAULT_NONLOGIN_SHELL_CONFIG_FILE = NONLOGIN_SHELL_CONFIG_FILES[0]

    MODE = "mode"
    SYSTEMS_TYPE = "systems_type"
    DESKTOP = "desktop"
    SERVER = "server"
    UNINSTALL = "uninstall"
    INSTALL = "install"
    PYTHONPATH = "PYTHONPATH"
    EMPTY_PATH = ""

    def __init__(self):

        self.os_name = platform.system().lower()
        self.pythonpath = os.environ.get(self.PYTHONPATH, self.EMPTY_PATH)

        self.current_user_home = os.path.expanduser("~")
        self.user_bin_path = os.path.expanduser(
            f"{self.current_user_home}/.local/bin"
        )
        self.user_bin_exist = pathlib.Path(self.user_bin_path).exists()

        self.link_path = join(self.user_bin_path, PROGRAM_NAME)
        self.installed = (
            True
            if (
                pathlib.Path(self.link_path).exists()
                and ROOTDIR in self.pythonpath
            )
            else False
        )

    def retrieve_args(self):

        self._parser.add_argument(
            f"--{self.DESKTOP}",
            action="store_const",
            const=self.DESKTOP,
            default=self.SERVER,
            dest=self.SYSTEMS_TYPE,
            help="runs the installer for OSES with a DE",
        )
        self._parser.add_argument(
            f"--{self.UNINSTALL}",
            action="store_const",
            const=self.UNINSTALL,
            default=self.INSTALL,
            dest=self.MODE,
            help="specifies the mode to run installer in",
        )
        args = vars(self._parser.parse_args())
        self.systems_type = args[self.SYSTEMS_TYPE]
        self.mode = args[self.MODE]

    def install(self):

        if self.os_name not in self.SUPPORTED_OSES:
            print(
                f"{ERROR_PREFIX} {self.os_name} is not currently supported for {PROGRAM_NAME}."
            )
        else:
            if not self.user_bin_exist:
                os.mkdir(self.user_bin_path)
            os.symlink(EXECUTABLE_LOCATION, self.link_path)
            if self.systems_type is self.SERVER:
                self._write_to_startupfile(
                    self.LOGIN_SHELL_CONFIG_FILES,
                    self.DEFAULT_LOGIN_SHELL_CONFIG_FILE,
                )
            else:
                self._write_to_startupfile(
                    self.NONLOGIN_SHELL_CONFIG_FILES,
                    self.DEFAULT_NONLOGIN_SHELL_CONFIG_FILE,
                )

    def uninstall(self):

        os.remove(self.link_path)
        print(f"Uninstalled {PROGRAM_NAME} successfully!")
        print(
            f"Edit shell startup files to remove {PROGRAM_NAME} from PYTHONPATH."
        )

    def _write_to_startupfile(self, shell_startup_files, default_startup_file):

        for startup_file in shell_startup_files:
            startup_file_path = join(self.current_user_home, startup_file)
            startup_file_exists = pathlib.Path(startup_file_path).exists()
            if (
                not startup_file_exists
                and startup_file is shell_startup_files[-1]
            ):
                # Could not find a startup file that exists
                # So create default startup file
                default_path = join(
                    self.current_user_home, default_startup_file
                )
                open(default_path, "a").close()
                startup_file_path = default_path
            if pathlib.Path(startup_file_path).exists():
                if self.pythonpath is self.EMPTY_PATH:
                    self.pythonpath_to_set = ROOTDIR
                else:
                    self.pythonpath = self.pythonpath.split(os.pathsep)
                    self.pythonpath.insert(0, ROOTDIR)
                    self.pythonpath_to_set = os.pathsep.join(self.pythonpath)

                with open(startup_file_path, "a") as f:
                    f.write(f"# >>> {PROGRAM_NAME} initialize >>>\n")
                    f.write(
                        f"export {self.PYTHONPATH}={self.pythonpath_to_set}"
                    )
                    f.write("\n")
                    f.write(f"# <<< {PROGRAM_NAME} initialize <<<\n")
                    f.close()
                break


if __name__ == "__main__":
    installer = Installer()
    installer.retrieve_args()
    if installer.mode is installer.UNINSTALL and installer.installed:
        installer.uninstall()
    elif installer.mode is installer.UNINSTALL and not installer.installed:
        print(f"{ERROR_PREFIX} {PROGRAM_NAME} is not installed!")
    elif installer.mode is installer.INSTALL and installer.installed:
        print(f"{ERROR_PREFIX} {PROGRAM_NAME} is already installed!")
    else:
        installer.install()

