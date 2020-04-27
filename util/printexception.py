# Standard Library Imports
import os, subprocess
from os.path import realpath

# Third Party Imports

# Local Application Imports

class PrintException():

    PERMISSION_DENIED_MESSAGE = "Error: a particular file/path was unaccessable, "
    FILE_NOTFOUND_MESSAGE = "Error: a particular file/path was unaccessable, "

    @classmethod
    def print_permission_denied(cls, filename):

        print(f"{cls.PERMISSION_DENIED_MESSAGE}'{realpath(filename)}'")

    @classmethod
    def print_file_notfound(cls, filename):

        print(f"{cls.FILE_NOTFOUND_MESSAGE}'{realpath(filename)}'")

    @classmethod
    def print_toml_decodeerror(cls, exception):

        print("Error: the configuration file contains syntax error(s), more details below")
        print(exception)

    @classmethod
    def print_key_error(cls, table_name):

        print(f"Error: {table_name} table does not exist in the configuration file")