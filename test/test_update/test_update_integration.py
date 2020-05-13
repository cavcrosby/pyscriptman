# Standard Library Imports
import subprocess, os, filecmp, sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.test_variables import PYREPOMAN_MAIN_PATH
from test.conftest import (
    localhost_clone_repo,
    remotehost_clone_repo,
    localhost_setup,
    remotehost_setup,
)
from test.test_update.conftest import (
    UPDATE_TARGET,
    MODEL_TARGET,
    ACTION_IDENTIFIER,
    configholder,
    finish_setup,
)


class TestUpdate:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(localhost_clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_update_localhost(self, localhost_setup):
        finish_setup()
        os.chdir(UPDATE_TARGET)
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER])
        os.chdir("..")
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(remotehost_clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_update_remotehost(self, remotehost_setup):
        finish_setup()
        os.chdir(UPDATE_TARGET)
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER])
        os.chdir("..")
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False
