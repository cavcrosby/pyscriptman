# Standard Library Imports
import subprocess, os, stat, filecmp
from os.path import join, realpath, dirname

# Third Party Imports
import pytest

# Local Application Imports
from pyrepoman.actions.update import Update
from util.printexception import PrintException
from util.diff import Diff
from test.test_update.conftest import (
    UPDATE_TARGET,
    MODEL_TARGET,
)


class TestUpdate:
    def test_update(self, normal_setup):

        update = Update()
        update.run()
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "change_filemode_win_linux",
        [
            [
                UPDATE_TARGET,  # testing update with a directory that does not have write access
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
            [
                join(UPDATE_TARGET, ".git"),  # testing pyrepoman update with a working directory's .git directory having no write access
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
        indirect=["change_filemode_win_linux"],
    )
    def test_update_calledprocesserror_handled(self, change_filemode_win_linux):

        with pytest.raises(subprocess.CalledProcessError):
            update = Update()
            update.run()

    @pytest.mark.parametrize(
        "change_filemode_win_linux",
        [
            [
                dirname(realpath(UPDATE_TARGET)),  # testing update with a directory whose parent has no read permissions
                stat.S_IWUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH,  # permissions == filemode 377
                stat.S_IREAD,
            ],
            [
                UPDATE_TARGET,  # testing update with a directory that does not have execute permissions
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
        indirect=["change_filemode_win_linux"],
    )
    def test_update_permissionerror_handled(self, change_filemode_win_linux, capsys):

        with pytest.raises(PermissionError):
            update = Update()
            update.run()

        out, err = capsys.readouterr()
        assert PrintException.PERMISSION_DENIED_MESSAGE in out

    def test_update_file_notfound_handled(self, normal_setup, capsys, monkeypatch):

        from pyrepoman.actions.action import Action

        def fake_get_pwd_local_nonbare_repo_names(cls):

            return "non-existing git repo"

        monkeypatch.setattr(
            Action,
            "_get_pwd_local_nonbare_repo_names",
            fake_get_pwd_local_nonbare_repo_names,
        )

        with pytest.raises(FileNotFoundError):
            update = Update()
            update.run()

        out, err = capsys.readouterr()
        assert PrintException.FILE_NOTFOUND_MESSAGE in out
