# Standard Library Imports
from abc import ABC, abstractmethod, abstractclassmethod
import os, subprocess, shutil

# Third Party Imports

# Local Application Imports

class Host(ABC):

    _HELP_DESC = NotImplemented

    @property
    def repo_names_and_locations(self):

        return self._repo_names_and_locations

    def __init__(self):
        self._repo_names_and_locations = dict()

    def __init_subclass__(cls, *args, **kwargs):

        super().__init_subclass__(*args, **kwargs)

        if cls._HELP_DESC is NotImplemented:
            raise NotImplementedError(f'Error: _HELP_DESC not defined in {cls.__name__}')

    @staticmethod
    def _get_pwd_local_dir_names():

        root = os.getcwd()
        return [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]

    @classmethod
    def _get_pwd_bare_repo_names(cls, host_path):
            
            repos = list()
            pwd = os.getcwd()
            os.chdir(host_path)
            dirs = cls._get_pwd_local_dir_names()
            for dir in dirs:
                os.chdir(dir)
                is_bare_repo = subprocess.run(['git', 'rev-parse', '--is-bare-repository'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
                in_working_dir = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
                if(is_bare_repo.stderr == '' and is_bare_repo.stdout.rstrip() == 'true' and in_working_dir.stdout.rstrip() == 'false'):
                    repos.append(dir)
                os.chdir('..')
            os.chdir(pwd)
            return repos

    @classmethod
    def add_parser(cls, subparser_container, help_desc):

        subcommand = cls.__name__.lower()
        parser = subparser_container.add_parser(subcommand, help=help_desc, allow_abbrev=False)
        parser = cls._modify_parser(parser)
        parser.set_defaults(host=subcommand)
        return parser
        
    def add_repo_name_and_location(self, repo_name, location):

        self.repo_names_and_locations[repo_name] = location

    def get_location_from_repo_name(self, repo_name):

        return self.repo_names_and_locations[repo_name]

    @abstractclassmethod
    def is_host_type(cls, identifier):

        """ FUNCTION USED ALONG WITH THE _IDENTIFIER TO DETERMINE IF PASSED IN HOST IS OF TYPE """
        
        pass
    
    @abstractclassmethod
    def _modify_parser(cls, parser):

        pass

    @abstractmethod
    def get_user_repo_names_and_locations(self):

        """ RANGE OF THIS FUNCTION IS REPO_NAME (KEY) --> REPO_LOCATION (VALUE) DATA STRUCTURE """

        pass
