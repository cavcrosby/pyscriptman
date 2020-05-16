# Standard Library Imports
import os, subprocess
from os.path import realpath

# Third Party Imports

# Local Application Imports


class PrintMessage:

    ERROR_PREFIX = "Error:"
    WARNING_PREFIX = "Warning:"
    UNKNOWN_ERROR_OCCURRED = (
        "an unknown error occurred, please report the following below:"
    )
    PERMISSION_DENIED_MESSAGE = "a particular file/path was unaccessable,"
    FILE_NOTFOUND_MESSAGE = "a particular file/path was unaccessable,"
    TOML_DECODEERROR_MESSAGE = (
        "the configuration file contains syntax error(s), more details below"
    )
    TABLE_DOES_NOT_EXIST_MESSAGE = "table does not exist in the configuration file"
    REQUESTS_PACKAGE_CONNECTIONERROR_MESSAGE = (
        "check network settings or try again later, failed to connect to:"
    )
    REQUESTS_PACKAGE_HTTPERROR_MESSAGE = (
        "communication with webhost failed, webhost/error message:"
    )
    SCRIPT_REMOVAL_FAILED_MESSAGE = "could not remove script from: "
    CONFIGHOLDER_RECEIVED_DUP_CONFIG_MESSAGE = (
        "configholder was given a duplicate configuration to store:"
    )
    CONFIGHOLDER_CONFIG_NOT_EXIST = "configuration does not exist,"

    @classmethod
    def print_unknown_error_occurred(cls, exception):

        print(f"{cls.ERROR_PREFIX} {cls.UNKNOWN_ERROR_OCCURRED}")
        print(exception)

    @classmethod
    def print_permission_denied(cls, filename):

        print(
            f"{cls.ERROR_PREFIX} {cls.PERMISSION_DENIED_MESSAGE} '{realpath(filename)}'"
        )

    @classmethod
    def print_file_notfound(cls, filename):

        print(f"{cls.ERROR_PREFIX} {cls.FILE_NOTFOUND_MESSAGE} '{realpath(filename)}'")

    @classmethod
    def print_toml_decodeerror(cls, exception):

        print(f"{cls.ERROR_PREFIX} {cls.TOML_DECODEERROR_MESSAGE}")
        print(exception)

    @classmethod
    def print_table_not_exist(cls, table_name):

        print(f"{cls.ERROR_PREFIX} '{table_name}' {cls.TABLE_DOES_NOT_EXIST_MESSAGE}")

    @classmethod
    def print_requests_connectionerror(cls, class_name):

        print(
            f"{cls.ERROR_PREFIX} {cls.REQUESTS_PACKAGE_CONNECTIONERROR_MESSAGE} '{class_name}'"
        )

    @classmethod
    def print_requests_httperror(cls, class_name, response):

        print(
            f"{cls.ERROR_PREFIX} {cls.REQUESTS_PACKAGE_HTTPERROR_MESSAGE} {class_name}/{response.json()['message']}"
        )

    @classmethod
    def print_script_removal_fail(cls, target):

        print(f"{cls.WARNING_PREFIX} {cls.SCRIPT_REMOVAL_FAILED_MESSAGE} '{target}'")

    @classmethod
    def print_configholder_duplicate_config_inserted(cls, config_name, value):

        print(
            f"{cls.WARNING_PREFIX} {cls.CONFIGHOLDER_RECEIVED_DUP_CONFIG_MESSAGE} {config_name} {value}"
        )

    @classmethod
    def print_configuration_not_exist(cls, config_name):

        print(f"{cls.ERROR_PREFIX} {cls.CONFIGHOLDER_CONFIG_NOT_EXIST} {config_name}")
