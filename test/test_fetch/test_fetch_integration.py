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
    localhost_setup,
    remotehost_setup,
    FETCH_TARGET,
    MODEL_TARGET,
    ACTION_IDENTIFIER,
    configholder,
)


class TestFetch:
    def test_fetch_localhost(self, localhost_setup):
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "localhost",
                configholder.get_config_value("BARE_REPOS_DIR"),
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    def test_fetch_remotehost(self, remotehost_setup):
        target = f"{configholder.get_config_value('REMOTE_USER')}@{configholder.get_config_value('REMOTE_ADDR')}"
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "remotehost",  # TODO IF REMOTEHOST CANNOT BE REACHED, MAKE SURE TEST FAILS THEN!
                target,
                "--target-path",
                configholder.get_config_value('REMOTE_BARE_REPOS_DIR'),
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            ("own", "all"),
            ("own", "public"),
            ("own", "private"),
        ],
        indirect=True,
    )
    def test_fetch_github_own(self, github_setup):
        data = github_setup
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "github",
                repo_owner_type,
                "--repo-type",
                repo_type,
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            ("other", "all"),
            ("other", "owner"),
            ("other", "member"),
        ],
        indirect=True,
    )
    def test_fetch_github_other(self, github_setup):
        data = github_setup
        username = configholder.get_config_value("GITHUB_NAME")
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "github",
                repo_owner_type,
                username,
                "--repo-type",
                repo_type,
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False
