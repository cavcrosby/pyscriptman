"""Class module for configurations."""
# Standard Library Imports

# Third Party Imports

# Local Application Imports


class Config:
    """How configurations are created.
    
    Parameters
    ----------
    name : str
        Name of the configuration.
    value : str
        Value of the configuration.

    """

    @property
    def name(self):
        """Getter for configuration name."""
        return self._name

    @property
    def value(self):
        """Getter for configuration value."""
        return self._value

    def __init__(self, name, value):

        self._name = name
        self._value = value
