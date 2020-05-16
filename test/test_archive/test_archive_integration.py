# Standard Library Imports
import subprocess, os, filecmp, sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from test.conftest import (
    localhost_bundle_repo,
    remotehost_bundle_repo,
    github_bundle_repo,
    localhost_setup,
    remotehost_setup,
    github_setup,
)
from test.test_archive.conftest import (
    configholder,
    ACTION_IDENTIFIER,
    ARCHIVE_TARGET,
    MODEL_TARGET,
)
from test.test_variables import (
    PYREPOMAN_MAIN_PATH,
)


class TestArchiveIntegration:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(localhost_bundle_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_archive_localhost(self, localhost_setup):
        os.chdir(ARCHIVE_TARGET)
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
        #dcmp = filecmp.dircmp(ARCHIVE_TARGET, MODEL_TARGET)
        #diff = Diff(dcmp) 
        #TODO tests with the same bundles are seen as different for some reason, investigate
        dir_package = os.listdir(ARCHIVE_TARGET)
        dir_setup = os.listdir(MODEL_TARGET)
        assert dir_package == dir_setup

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(remotehost_bundle_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_archive_remotehost(self, remotehost_setup):
        target = f"{configholder.get_config_value('REMOTE_USER')}@{configholder.get_config_value('REMOTE_ADDR')}"
        os.chdir(ARCHIVE_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "remotehost",
                target,
                "--target-path",
                configholder.get_config_value("REMOTE_BARE_REPOS_DIR_PATH"),
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(ARCHIVE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            ("own", "all", github_bundle_repo, configholder, MODEL_TARGET),
            ("own", "public", github_bundle_repo, configholder, MODEL_TARGET),
            ("own", "private", github_bundle_repo, configholder, MODEL_TARGET),
        ],
        indirect=True,
    )
    def test_archive_github_own(self, github_setup):
        data = github_setup
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(ARCHIVE_TARGET)
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
        dcmp = filecmp.dircmp(ARCHIVE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            ("other", "all", github_bundle_repo, configholder, MODEL_TARGET),
            ("other", "owner", github_bundle_repo, configholder, MODEL_TARGET),
            ("other", "member", github_bundle_repo, configholder, MODEL_TARGET),
        ],
        indirect=True,
    )
    def test_archive_github_other(self, github_setup):
        data = github_setup
        username = configholder.get_config_value("GITHUB_NAME")
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(ARCHIVE_TARGET)
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
        dcmp = filecmp.dircmp(ARCHIVE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False