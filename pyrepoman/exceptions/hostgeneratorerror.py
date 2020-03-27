# Standard Library Imports

# Third Party Imports

# Local Application Imports

class HostGeneratorError(Exception):

    def __init__(self, message, configholder):

        super().__init__(message)
        self.host = configholder.get_config_value('host')
        self.host_path = configholder.get_config_value('host_path')
        self.path = configholder.get_config_value('path')
