# Standard Library Imports
import subprocess, sys, os, platform, stat
from os.path import join, realpath, dirname

# Third Party Imports
import pytest

# Local Application Imports
from pyrepoman.actions.update import Update
from util.printexception import PrintException
from test.test_update.conftest import (
    UPDATE_TARGET,
)
from test.test_variables import PYREPOMAN_MAIN_PATH
from test.helpers import change_target_filemode_recursive


class TestUpdate:
    @pytest.mark.parametrize(
        "change_filemode_win_linux",
        [
            [
                UPDATE_TARGET, # testing update with a directory that does not have write access
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH, # permissions == filemode 577
                stat.S_IREAD
            ],
            [
                join(UPDATE_TARGET, '.git'), # testing pyrepoman update with a working directory's .git directory having no write access
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH, # permissions == filemode 577
                stat.S_IREAD
            ]
        ],
        indirect=["change_filemode_win_linux"]
    )
    def test_calledprocesserror_handled(self, change_filemode_win_linux):

        with pytest.raises(subprocess.CalledProcessError):
            update = Update()
            update.run()
    
    @pytest.mark.parametrize(
        "change_filemode_win_linux",
        [
            [
                dirname(realpath(UPDATE_TARGET)), # testing update with a directory whose parent has no read permissions
                stat.S_IWUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH, # permissions == filemode 377
                stat.S_IREAD
            ],
            [
                UPDATE_TARGET, # testing update with a directory that does not have execute permissions
                stat.S_IRUSR
                | stat.S_IWUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IWOTH
                | stat.S_IXOTH, # permissions == filemode 677
                stat.S_IREAD
            ]
        ],
        indirect=["change_filemode_win_linux"]
    )
    def test_permissionerror_handled(self, change_filemode_win_linux, capsys):

        with pytest.raises(PermissionError):
            update = Update()
            update.run()

        out, err = capsys.readouterr()
        assert PrintException.PERMISSION_DENIED_MESSAGE in out
