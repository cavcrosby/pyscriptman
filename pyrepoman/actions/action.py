# Standard Library Imports
from abc import ABC, abstractclassmethod
import os, subprocess, shutil

# Third Party Imports

# Local Application Imports

class Action(ABC):

    @staticmethod
    def _get_pwd_local_dir_names():

        #TODO os.listdir() CAN RETURN PERMISSION DENIED (e.g. if directory is not readable, but can be executable), SHOULD WE LOG THIS? (AN EXCEPTION HANDLER IS ALREADY IN PLACE)
        root = os.getcwd()
        return [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]

    @staticmethod
    def _remove_dir(dir_name):
        
        shutil.rmtree(dir_name)

    @staticmethod
    def _dir_exist(dir_name):
        
        dir_contents = os.listdir()
        return dir_name in dir_contents

    @staticmethod
    def _create_mirror(url, destination_dir_name):
        
        subprocess.run(["git", "clone", "--mirror", url, destination_dir_name], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

    @staticmethod
    def _update_mirror(dir_name):
        
        subprocess.run(["git", "--git-dir", dir_name, "remote", "update"])

    @staticmethod
    def _create_bundle(repo_bundle_name, mirror_repo):
        
        subprocess.run(["git", "--git-dir", mirror_repo, "bundle", "create", f"{repo_bundle_name}.bundle", "--all"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

    @classmethod
    def _get_pwd_local_nonbare_repo_names(cls):
        
        repos = list()
        dirs = cls._get_pwd_local_dir_names()
        for dir in dirs:
            os.chdir(dir)
            is_bare_repo = subprocess.run(['git', 'rev-parse', '--is-bare-repository'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            in_working_dir = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            if(is_bare_repo.stderr == '' and is_bare_repo.stdout.rstrip() == 'false' and in_working_dir.stdout.rstrip() == 'true'):
                repos.append(dir)
            os.chdir('..')
        return repos

    @classmethod
    def _remove_all_dir_content(cls, dir_name, exclude = None):
        
        os.chdir(dir_name)
        nodes = os.scandir()
        try:
            dir_entry = nodes.__next__()
            if(exclude == None):
                exclude = list()
            while(dir_entry):
                if(dir_entry.name in exclude):
                    dir_entry = nodes.__next__()
                    continue
                if(dir_entry.is_dir()):
                    cls._remove_dir(dir_entry.name)
                    dir_entry = nodes.__next__()
                else:
                    os.remove(dir_entry)
                    dir_entry = nodes.__next__()
        except StopIteration as e:
            pass
        finally:
            os.chdir('..')

    @classmethod
    def _create_dir(cls, dir_name):

        if(not cls._dir_exist(dir_name)):
            os.mkdir(dir_name)

    @classmethod
    def is_action_type(cls, identifier):

        if(identifier == cls._get_identifier()):
            return True

        return False

    @classmethod
    def _get_identifier(cls):

        """ USED TO HELP GENERATOR DETERMINE WHAT ACTION TO CREATE """
        
        return cls.__name__.lower()
    
    @abstractclassmethod
    def run(cls):

        """ HOW EACH ACTION IS TO PERFORM ITS FUNCTIONALITY """

        pass
