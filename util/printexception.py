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

    @classmethod
    def print_script_removal_fail_warning(cls, target):

        print(f"Warning: could not remove script from {target}")

    @classmethod
    def print_attribute_error(cls, exception):

        print(f"Error: {exception.args[0]}")

    @classmethod
    def print_requests_connectionerror(cls, class_name):

        print(f"Error: could not connect to {class_name}, check network settings or try again later")

    @classmethod
    def print_requests_httperror(cls, class_name, response):

        print(f"Error: communicating with {class_name} failed; Reason: {response.json()['message']}")
