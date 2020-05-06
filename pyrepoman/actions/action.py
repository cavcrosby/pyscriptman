# Standard Library Imports
from abc import ABC, abstractclassmethod
import os, subprocess, shutil, re, sys

# Third Party Imports

# Local Application Imports
from pyrepoman.helpers import get_pwd_typeof_repo_names
from util.printexception import PrintException


class Action(ABC):

    HELP_DESC = NotImplemented

    _HOST_SUBPARSER_TITLE = "available actions"
    _HOST_SUBPARSER_METAVAR = "action [options ...]"
    _REQUIRE_SUBCOMMANDS = True

    def __init_subclass__(cls, *args, **kwargs):

        super().__init_subclass__(*args, **kwargs)

        if cls.HELP_DESC is NotImplemented:
            raise NotImplementedError(f"Error: HELP_DESC not defined in {cls.__name__}")

    @staticmethod
    def _remove_dir(dir_name):

        shutil.rmtree(dir_name)

    @staticmethod
    def _dir_exist(dir_name):

        dir_contents = os.listdir()
        return dir_name in dir_contents

    @staticmethod
    def _update_mirror(dir_name):

        subprocess.run(["git", "--git-dir", dir_name, "remote", "update"])

    @classmethod
    def _create_bundle(cls, repo_bundle_name, mirror_repo):

        completed_process = subprocess.run(
            [
                "git",
                "--git-dir",
                mirror_repo,
                "bundle",
                "create",
                f"{repo_bundle_name}.bundle",
                "--all",
            ]
        )
        completed_process.check_returncode()

    @classmethod
    def _create_mirror(cls, location, destination_dir_name):

        completed_process = subprocess.run(
            ["git", "clone", "--mirror", location, destination_dir_name],
        )
        completed_process.check_returncode()

    @staticmethod
    def _get_pwd_local_nonbare_repo_names():

        return get_pwd_typeof_repo_names(os.getcwd(), False)

    @classmethod
    def _remove_all_dir_content(cls, dir_name, exclude=None):

        os.chdir(dir_name)
        nodes = os.scandir()
        try:
            dir_entry = nodes.__next__()
            if exclude == None:
                exclude = list()
            while dir_entry:
                if dir_entry.name in exclude:
                    dir_entry = nodes.__next__()
                    continue
                if dir_entry.is_dir():
                    cls._remove_dir(dir_entry.name)
                    dir_entry = nodes.__next__()
                else:
                    os.remove(dir_entry)
                    dir_entry = nodes.__next__()
        except StopIteration:
            pass
        except PermissionError as e:
            PrintException.print_permission_denied(e.filename)
            sys.exit(e.errno)
        finally:
            os.chdir("..")

    @classmethod
    def _create_dir(cls, dir_name):

        if not cls._dir_exist(dir_name):
            os.mkdir(dir_name)

    @classmethod
    def is_action_type(cls, chosen_action):

        return chosen_action == cls._get_action_name()

    @classmethod
    def _get_action_name(cls):

        return cls.__name__.lower()

    @classmethod
    def add_parser(cls, subparser_container, help_desc):

        subcommand = cls._get_action_name()
        parser = subparser_container.add_parser(
            subcommand, help=cls.HELP_DESC, allow_abbrev=False
        )
        parser = cls._modify_parser(parser)
        parser.set_defaults(action=subcommand)
        return parser

    @abstractclassmethod
    def _modify_parser(cls, parser):

        pass

    @abstractclassmethod
    def run(cls):

        """ HOW EACH ACTION IS TO PERFORM ITS FUNCTIONALITY """

        pass
