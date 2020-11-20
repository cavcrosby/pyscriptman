# Standard Library Imports
import subprocess
import os
import stat
import filecmp
from os.path import join, realpath, dirname

# Third Party Imports
import pytest

# Local Application Imports
from pyscriptman.actions.update import Update
from util.message import Message
from util.diff import Diff
from util.helpers import clone_repo
from test.test_update.conftest import (
    UPDATE_TARGET,
    MODEL_TARGET,
    configholder,
    finish_setup,
)


class TestUpdateUnit:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_update(self, localhost_setup):
        """Testing the update functionality with a Git repo.
        
        This Git repo is also on the local
        computer.
        
        """
        finish_setup()
        os.chdir(UPDATE_TARGET)
        update = Update()
        update.run()
        os.chdir("..")
        dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() is False

    def test_update_file_notfound_handled(
        self, unit_test_setup, capsys, monkeypatch
    ):
        """Testing the update functionality with a FileNotFound exception.
        
        To ensure such an exception is handled by the
        update action. This involves printing a custom
        message related to the FileNotFound error.

        """
        from pyscriptman.actions.action import Action

        def fake_get_bare_repo_names_from_path(arg1):

            return "non-existing git repo"

        monkeypatch.setattr(
            Action,
            "_get_pwd_local_nonbare_repo_names",
            fake_get_bare_repo_names_from_path,
        )

        with pytest.raises(FileNotFoundError):
            update = Update()
            update.run()

        out, err = capsys.readouterr()
        assert Message.FILE_NOTFOUND_MESSAGE in out

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
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
                realpath(
                    join(UPDATE_TARGET, ".git")
                ),  # testing update with a working directory's .git directory having no write access
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
    def test_update_calledprocesserror_handled(
        self, filemode_change_setup_win_linux
    ):
        """Testing the update functionality with a CalledProcessError exception.
        
        Specifically the subprocess.CalledProcessError is
        tested for to ensure that the update action
        raises the exception.

        """
        with pytest.raises(subprocess.CalledProcessError):
            update = Update()
            update.run()

    @pytest.mark.parametrize(
        "filemode_change_setup_win_linux",
        [
            [
                dirname(
                    realpath(UPDATE_TARGET)
                ),  # testing update with a directory whose parent has no read permissions
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
        indirect=["filemode_change_setup_win_linux"],
    )
    def test_update_permissionerror_handled(
        self, filemode_change_setup_win_linux, capsys
    ):
        """Testing the update functionality with a PermissionError exception.
        
        To ensure such an exception is handled by the
        update action. This involves printing a custom
        message related to the PermissionError.

        """
        with pytest.raises(PermissionError):
            update = Update()
            update.run()

        out, err = capsys.readouterr()
        assert Message.PERMISSION_DENIED_MESSAGE in out
