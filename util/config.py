# Standard Library Imports
import sys

# Third Party Imports
import toml

# Local Application Imports
from util.message import Message


class Config:
    @property
    def name(self):

        return self._name

    @property
    def value(self):

        return self._value

    def __init__(self, name, value):

        self._name = name
        self._value = value
