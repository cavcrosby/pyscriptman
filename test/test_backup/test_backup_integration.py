# Standard Library Imports
import subprocess
import os
import filecmp
import sys

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from pyrepoman.hosts.webhosts.github import GitHub
from util.helpers import mirror_repo
from test.test_backup.conftest import (
    configholder,
    ACTION_IDENTIFIER,
    BACKUP_TARGET,
    MODEL_TARGET,
)
from test.test_variables import PYREPOMAN_MAIN_PATH


class TestBackupIntegration:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(mirror_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_backup_localhost(self, localhost_setup):
        """Testing the backup functionality with a LocalHost host.
        
        Same as unit test but encompassed by the
        entire program.
        
        """
        os.chdir(BACKUP_TARGET)
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
        dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(mirror_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_backup_remotehost(self, remotehost_setup):
        """Testing the backup functionality with a RemoteHost host."""
        target = f"{configholder.get_config_value('REMOTE_USER')}@{configholder.get_config_value('REMOTE_ADDR')}"
        os.chdir(BACKUP_TARGET)
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
        dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OWN_CMD_ARG_NAME,
                "all",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "public",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "private",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_backup_github_own(self, github_setup):
        """Testing the backup functionality with a GitHub host.
        
        This includes all of the GitHub host
        options with the own subcommand.
        
        """
        data = github_setup
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(BACKUP_TARGET)
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
        dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "all",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "owner",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "member",
                mirror_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_backup_github_other(self, github_setup):
        """Testing the backup functionality with a GitHub host.
        
        This includes all of the GitHub host
        options with the other subcommand.
        
        """
        data = github_setup
        username = configholder.get_config_value("GITHUB_USERNAME")
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(BACKUP_TARGET)
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
        dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False
