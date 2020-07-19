# Standard Library Imports
import subprocess
import os
import filecmp
import sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.test_variables import PYREPOMAN_MAIN_PATH
from util.helpers import clone_repo
from test.test_update.conftest import (
    UPDATE_TARGET,
    MODEL_TARGET,
    ACTION_IDENTIFIER,
    configholder,
    finish_setup,
)


class TestUpdateIntegration:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_update_localhost(self, localhost_setup):
        """Testing the update functionality with Git repo.
        
        Same as unit test but encompassed by the
        entire program. Git repo is also on the local
        computer.
        
        """
        finish_setup()
        os.chdir(UPDATE_TARGET)
        subprocess.run(
            [sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_update_remotehost(self, remotehost_setup):
        """Testing the update functionality with a Git repo.
        
        Git repo will be pulled from a remote host.
        
        """
        finish_setup()
        os.chdir(UPDATE_TARGET)
        subprocess.run(
            [sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False
