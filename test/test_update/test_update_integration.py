# Standard Library Imports
import subprocess, os, filecmp, sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.test_variables import PYREPOMAN_MAIN_PATH
from test.test_update.conftest import (
    normal_setup,
    UPDATE_TARGET,
    MODEL_TARGET,
    ACTION_IDENTIFIER,
)


class TestUpdate:
    def test_update_localhost(self, normal_setup):
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER])
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    def test_update_remotehost(self, normal_setup):
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER])
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False
