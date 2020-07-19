# Standard Library Imports
import subprocess
import os
import sys

# Third Party Imports
import pytest

# Local Application Imports
from pyrepoman.hosts.webhosts.github import GitHub
from util.helpers import bundle_repo
from test.test_archive.conftest import (
    configholder,
    ACTION_IDENTIFIER,
    ARCHIVE_TARGET,
    MODEL_TARGET,
    diff_bundle_contents,
)
from test.test_variables import PYREPOMAN_MAIN_PATH


class TestArchiveIntegration:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(bundle_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_archive_localhost(self, localhost_setup):
        """Testing the archive functionality with a LocalHost host.
        
        Same as unit test but encompassed by the
        entire program.
        
        """
        os.chdir(ARCHIVE_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "localhost",
                configholder.get_config_value("LOCAL_BARE_REPOS_DIR_PATH"),
            ]
        )
        os.chdir("..")
        assert diff_bundle_contents() is False

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(bundle_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_archive_remotehost(self, remotehost_setup):
        """Testing the archive functionality with a RemoteHost host."""
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
        assert diff_bundle_contents() is False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OWN_CMD_ARG_NAME,
                "all",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "public",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "private",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_archive_github_own(self, github_setup):
        """Testing the archive functionality with a GitHub host.
        
        This includes all of the GitHub host
        options with the own subcommand.
        
        """
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
        assert diff_bundle_contents() is False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "all",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "owner",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "member",
                bundle_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_archive_github_other(self, github_setup):
        """Testing the archive functionality with a GitHub host.
        
        This includes all of the GitHub host
        options with the other subcommand.
        
        """
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
        assert diff_bundle_contents() is False
