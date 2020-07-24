"""Used to organize messages printed through the project."""
# Standard Library Imports
from os.path import realpath

# Third Party Imports

# Local Application Imports


class Message:
    """Where messages are organized.

    Message constant names described the issue
    they pertain to.
    
    Attributes
    ----------
    ERROR_PREFIX : str
        Prefix appended to error messages.
    WARNING_PREFIX : str
        Prefix appended to warning messages.

    """

    ERROR_PREFIX = "Error:"
    WARNING_PREFIX = "Warning:"
    HELP_DESC_NOT_IMPLEMENTED = "HELP_DESC not defined in"
    UNKNOWN_ERROR_OCCURRED = (
        "an unknown error occurred, please report the following below:"
    )
    DEFAULT_TABLE_DOES_NOT_EXIST = (
        "entry does not exist, check the configuration file"
    )
    PERMISSION_DENIED_MESSAGE = "a particular file/path was unaccessable,"
    FILE_NOTFOUND_MESSAGE = "a particular file/path was unaccessable,"
    TOML_DECODEERROR_MESSAGE = (
        "the configuration file contains syntax error(s), more details below"
    )
    TABLE_DOES_NOT_EXIST_MESSAGE = (
        "table does not exist in the configuration file"
    )
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
    FACTORY_INVALID_ACTION = "Invalid action target; action"
    FACTORY_INVALID_HOST = "Invalid host target; Configs passed in:"

    @classmethod
    def construct_helpdesc_notimplemented_msg(cls, class_name):
        """Message for when a subclass does not implement HELP_DESC."""
        return (
            f"{cls.ERROR_PREFIX} {cls.HELP_DESC_NOT_IMPLEMENTED} {class_name}"
        )

    @classmethod
    def print_default_table_does_notexist(cls, default_table_name, table_name):
        """Message for when the default configurations table does not exist."""
        print(
            f"{cls.ERROR_PREFIX} [{table_name}.{default_table_name}] {cls.DEFAULT_TABLE_DOES_NOT_EXIST}"
        )

    @classmethod
    def print_unknown_error_occurred(cls, exception):
        """Message for when a unknown error occurs."""
        print(f"{cls.ERROR_PREFIX} {cls.UNKNOWN_ERROR_OCCURRED}")
        print(exception)

    @classmethod
    def print_permission_denied(cls, filename):
        """Message for when permission is denied."""
        print(
            f"{cls.ERROR_PREFIX} {cls.PERMISSION_DENIED_MESSAGE} '{realpath(filename)}'."
        )

    @classmethod
    def print_file_notfound(cls, filename):
        """Message for when a file is not found."""
        print(
            f"{cls.ERROR_PREFIX} {cls.FILE_NOTFOUND_MESSAGE} '{realpath(filename)}'."
        )

    @classmethod
    def print_toml_decodeerror(cls, excep_obj):
        """Message for when the loaded (toml) configuration file has a syntax error."""
        print(f"{cls.ERROR_PREFIX} {cls.TOML_DECODEERROR_MESSAGE}")
        print(excep_obj)

    @classmethod
    def print_table_not_exist(cls, table_name):
        """Message for when a table does not exist in the toml file."""
        print(
            f"{cls.ERROR_PREFIX} '{table_name}' {cls.TABLE_DOES_NOT_EXIST_MESSAGE}."
        )

    @classmethod
    def print_requests_connectionerror(cls, class_name):
        """Message for when requests library has a connection error."""
        print(
            f"{cls.ERROR_PREFIX} {cls.REQUESTS_PACKAGE_CONNECTIONERROR_MESSAGE} '{class_name}'."
        )

    @classmethod
    def print_requests_httperror(cls, class_name, response):
        """Message for when requests library has a http error."""
        print(
            f"{cls.ERROR_PREFIX} {cls.REQUESTS_PACKAGE_HTTPERROR_MESSAGE} {class_name}/{response.json()['message']}"
        )

    @classmethod
    def print_script_removal_fail(cls, target):
        """Message for when program fails to remove script from remote host."""
        print(
            f"{cls.WARNING_PREFIX} {cls.SCRIPT_REMOVAL_FAILED_MESSAGE} '{target}'."
        )

    @classmethod
    def print_configholder_duplicate_config_inserted(cls, config_name, value):
        """Message for when configholder receives a duplicate config to store."""
        print(
            f"{cls.WARNING_PREFIX} {cls.CONFIGHOLDER_RECEIVED_DUP_CONFIG_MESSAGE} {config_name} {value}."
        )

    @classmethod
    def print_configuration_not_exist(cls, config_name):
        """Message for when requested config does not exist in configholder."""
        print(
            f"{cls.ERROR_PREFIX} {cls.CONFIGHOLDER_CONFIG_NOT_EXIST} {config_name}."
        )

    @classmethod
    def print_factory_invalid_action(cls, action_name):
        """Message for when a invalid action is selected from command line."""
        print(
            f"{cls.ERROR_PREFIX} {cls.FACTORY_INVALID_ACTION} {action_name}."
        )

    @classmethod
    def print_factory_invalid_host(cls, configholder):
        """Message for when a invalid host is selected from command line."""
        print(f"{cls.ERROR_PREFIX} {cls.FACTORY_INVALID_HOST} {configholder}.")
