# Standard Library Imports
import subprocess, os, stat, filecmp
from os.path import join, expanduser, dirname

# Third Party Imports
import pytest, requests

# Local Application Imports
from pyrepoman.actions.archive import Archive
from pyrepoman.hosts.localhost import LocalHost
from pyrepoman.hosts.webhosts.github import GitHub
from util.printmessage import PrintMessage
from util.diff import Diff
from test.conftest import (
    localhost_clone_repo,
    localhost_setup,
    filemode_change_setup_win_linux,
)
from test.test_archive.conftest import (
    ARCHIVE_TARGET,
    MODEL_TARGET,
    configholder,
    unit_test_setup,
    configholder,
)


def generate_localhost():

    # see localhost constructor, as it is expecting a configuration called 'path'
    target_path = expanduser(configholder.get_config_value("BARE_REPOS_DIR"))
    configholder.add_config(
        "path", target_path
    )
    return LocalHost(configholder)

def generate_github_host():

    # see github constructor, as it is currently expecting the following configurations
    configholder.add_config("repo_type", "all")
    configholder.add_config("repo_owner_type", "own")
    configholder.add_config("username", configholder.get_config_value("GITHUB_NAME"))

    return GitHub(configholder)

def fake_get_user_repo_names_and_locations(self):

    self._get_user_repo_names_and_locations()

class TestArchiveUnit:
    def test_archive_file_notfound_handled(self, unit_test_setup, capsys, monkeypatch):

        from pyrepoman.hosts.host import Host

        def fake_get_pwd_local_nonbare_repo_names(arg1, arg2):

            os.chdir("non-existing git repo")

        monkeypatch.setattr(
            Host,
            "_get_pwd_bare_repo_names",
            fake_get_pwd_local_nonbare_repo_names,
        )

        with pytest.raises(FileNotFoundError):
            localhost = generate_localhost()
            archive = Archive(localhost)
            archive.run()

        out, err = capsys.readouterr()
        assert PrintMessage.FILE_NOTFOUND_MESSAGE in out

    def test_archive_requests_connectionerror_handled(self, unit_test_setup, capsys, monkeypatch):

        from pyrepoman.hosts.webhosts import github
        from pyrepoman.hosts.webhosts.webhost import WebHost

        class FakeGitHubAuth:

            def __init__(self, arg1):

                raise requests.exceptions.ConnectionError

        monkeypatch.setattr(
            github,
            "GitHubAuth",
            FakeGitHubAuth,
        )

        monkeypatch.setattr(
            WebHost,
            "get_user_repo_names_and_locations",
            fake_get_user_repo_names_and_locations,
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            github = generate_github_host()
            setattr(github, "api_token", "invalid-api-token")
            archive = Archive(github)
            archive.run()

        out, err = capsys.readouterr()
        assert PrintMessage.REQUESTS_PACKAGE_CONNECTIONERROR_MESSAGE in out

    def test_archive_requests_httperror_handled(self, unit_test_setup, capsys, monkeypatch):

        from pyrepoman.hosts.webhosts.webhost import WebHost

        monkeypatch.setattr(
            WebHost,
            "get_user_repo_names_and_locations",
            fake_get_user_repo_names_and_locations,
        )

        with pytest.raises(requests.exceptions.HTTPError):
            github = generate_github_host()
            setattr(github, "api_token", "invalid-api-token")
            archive = Archive(github)
            archive.run()

        out, err = capsys.readouterr()
        assert PrintMessage.REQUESTS_PACKAGE_HTTPERROR_MESSAGE in out

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
        [
            [
                expanduser(configholder.get_config_value("BARE_REPOS_DIR")),
                # testing archive with a path that does not have execute permissions
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
    def test_archive_permissionerror_handled(
        self, filemode_change_setup_win_linux, capsys
    ):

        with pytest.raises(PermissionError):
            localhost = generate_localhost()
            archive = Archive(localhost)
            archive.run()

        out, err = capsys.readouterr()
        assert PrintMessage.PERMISSION_DENIED_MESSAGE in out

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
        [
            [
                ARCHIVE_TARGET,  # testing archive with a directory that does not have write access
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
    def test_archive_calledprocesserror_handled(self, filemode_change_setup_win_linux):

        os.chdir(ARCHIVE_TARGET)

        with pytest.raises(subprocess.CalledProcessError):
            localhost = generate_localhost()
            archive = Archive(localhost)
            archive.run()

        os.chdir("..")
