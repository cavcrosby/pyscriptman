# Standard Library Imports
import subprocess, os, filecmp, sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.test_variables import PYREPOMAN_MAIN_PATH
from test.test_fetch.conftest import (
    normal_setup,
    github_setup,
    FETCH_TARGET,
    MODEL_TARGET,
    ACTION_IDENTIFIER,
)


class TestFetch:
    def test_fetch_localhost(self, normal_setup):
        os.chdir(FETCH_TARGET)
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER, "localhost", "~/Desktop/_pyrepoman"])
        os.chdir('..')
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    def test_fetch_remotehost(self, normal_setup):
        os.chdir(FETCH_TARGET)
        subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER, "remotehost", "git@192.168.254.234", "--target-path", "~/dev"])
        os.chdir('..')
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    # @pytest.mark.parametrize(
    #     "github_setup", 
    #     [
    #         ("own", "reap2sow1", "all"),
    #         ("own", "reap2sow1", "public"),
    #         ("own", "reap2sow1", "private"),
    #         ("other", "reap2sow1", "all"),
    #         ("other", "reap2sow1", "owner"),
    #         ("other", "reap2sow1", "member"),
    #     ],
    #     indirect=True
    # )
    # def test_fetch_github_own(self, github_setup):
    #     data = github_setup
    #     repo_owner_type, username, repo_type = data[0], data[1], data[2]
    #     os.chdir(FETCH_TARGET)
    #     if(repo_owner_type != "own"):
    #         subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER, "github", repo_owner_type, username, "--repo-type", repo_type])
    #     else:
    #         subprocess.run([sys.executable, PYREPOMAN_MAIN_PATH, ACTION_IDENTIFIER, "github", repo_owner_type, "--repo-type", repo_type])
    #     os.chdir("..")
    #     dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
    #     diff = Diff(dcmp)
    #     assert diff.run() == False
