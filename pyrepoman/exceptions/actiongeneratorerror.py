# Standard Library Imports

# Third Party Imports

# Local Application Imports

class ActionGeneratorError(Exception):

    def __init__(self, message, configholder):

        super().__init__(message)
        self.action = configholder.get_config_value('action')
