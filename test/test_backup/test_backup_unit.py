# Standard Library Imports
import subprocess, os, stat, filecmp
from os.path import join, expanduser, dirname

# Third Party Imports
import pytest, requests

# Local Application Imports
from pyrepoman.actions.backup import Backup
from util.printmessage import PrintMessage
from util.diff import Diff
from test.conftest import (
    localhost_mirror_repo,
    localhost_setup,
    filemode_change_setup_win_linux,
    generate_localhost,
    generate_github_host,
    fake_get_user_repo_names_and_locations,
)
from test.test_backup.conftest import (
    BACKUP_TARGET,
    MODEL_TARGET,
    configholder,
    unit_test_setup,
    configholder,
)


class TestBackupUnit:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(localhost_mirror_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_backup_localhost(self, localhost_setup):
        os.chdir(BACKUP_TARGET)
        localhost = generate_localhost(configholder)
        backup = Backup(localhost)
        backup.run()
        os.chdir("..")
        dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    def test_backup_file_notfound_handled(self, unit_test_setup, capsys, monkeypatch):

        from pyrepoman.hosts.host import Host

        def fake_get_pwd_local_nonbare_repo_names(arg1, arg2):

            os.chdir("non-existing git repo")

        monkeypatch.setattr(
            Host, "_get_pwd_bare_repo_names", fake_get_pwd_local_nonbare_repo_names,
        )

        with pytest.raises(FileNotFoundError):
            localhost = generate_localhost(configholder)
            backup = Backup(localhost)
            backup.run()

        out, err = capsys.readouterr()
        assert PrintMessage.FILE_NOTFOUND_MESSAGE in out

    def test_backup_requests_connectionerror_handled(
        self, unit_test_setup, capsys, monkeypatch
    ):

        from pyrepoman.hosts.webhosts import github
        from pyrepoman.hosts.webhosts.webhost import WebHost

        class FakeGitHubAuth:
            def __init__(self, arg1):

                raise requests.exceptions.ConnectionError

        monkeypatch.setattr(
            github, "GitHubAuth", FakeGitHubAuth,
        )

        monkeypatch.setattr(
            WebHost,
            "get_user_repo_names_and_locations",
            fake_get_user_repo_names_and_locations,
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            github = generate_github_host(configholder)
            setattr(github, "api_token", "invalid-api-token")
            backup = Backup(github)
            backup.run()

        out, err = capsys.readouterr()
        assert PrintMessage.REQUESTS_PACKAGE_CONNECTIONERROR_MESSAGE in out

    def test_backup_requests_httperror_handled(
        self, unit_test_setup, capsys, monkeypatch
    ):

        from pyrepoman.hosts.webhosts.webhost import WebHost

        monkeypatch.setattr(
            WebHost,
            "get_user_repo_names_and_locations",
            fake_get_user_repo_names_and_locations,
        )

        with pytest.raises(requests.exceptions.HTTPError):
            github = generate_github_host(configholder)
            setattr(github, "api_token", "invalid-api-token")
            backup = Backup(github)
            backup.run()

        out, err = capsys.readouterr()
        assert PrintMessage.REQUESTS_PACKAGE_HTTPERROR_MESSAGE in out

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
        [
            [
                expanduser(configholder.get_config_value("BARE_REPOS_DIR")),
                # testing backup with a path that does not have execute permissions
                stat.S_IRUSR
                | stat.S_IWUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH,  # permissions == filemode 677
                stat.S_IREAD,
            ],
        ],
        indirect=["filemode_change_setup_win_linux"],
    )
    def test_backup_permissionerror_handled(
        self, filemode_change_setup_win_linux, capsys
    ):

        with pytest.raises(PermissionError):
            localhost = generate_localhost(configholder)
            backup = Backup(localhost)
            backup.run()

        out, err = capsys.readouterr()
        assert PrintMessage.PERMISSION_DENIED_MESSAGE in out

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
        [
            [
                BACKUP_TARGET,  # testing backup with a directory that does not have write access
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH,  # permissions == filemode 577
                stat.S_IREAD,
            ],
        ],
        indirect=["filemode_change_setup_win_linux"],
    )
    def test_backup_calledprocesserror_handled(self, filemode_change_setup_win_linux):

        os.chdir(BACKUP_TARGET)

        with pytest.raises(subprocess.CalledProcessError):
            localhost = generate_localhost(configholder)
            backup = Backup(localhost)
            backup.run()

        os.chdir("..")
