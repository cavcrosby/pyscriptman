# Standard Library Imports
import sys

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message


class Config:
    @property
    def NAME(self):

        return self._name

    @property
    def VALUE(self):

        return self._value

    def __init__(self, name, value):

        self._name = name
        self._value = value
