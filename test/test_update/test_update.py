# Standard Library Imports
import subprocess, os, filecmp, sys

print(sys.path)

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.test_update.conftest import (
    pytest_runtest_setup,
    pytest_runtest_teardown,
    UPDATE_TARGET, 
    MODEL_TARGET, 
    ADDITIONAL_FILE1
)
from test.test_variables import (
    PYREPOMAN_MAIN_PATH,
)

class TestUpdate:
    def test_update_localhost(self):
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, "update"])
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    def test_update_remotehost(self):
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, "update"])
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False