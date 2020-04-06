# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports
from .host import Host
from ..global_variables import REMOTE_SCRIPT_GET_BARE_REPOS_NAME, REMOTE_SCRIPT_GET_BARE_REPOS_PATH

class RemoteHost(Host):

    def __init__(self, configholder):

        super().__init__()
        self.target = configholder.get_config_value('target')
        self.target_path = configholder.get_config_value('target_path')

    @staticmethod
    def expand_user_on_host(target, target_path):

        completed_process = subprocess.run(['ssh', target, f'python3 -c "import os; print(os.path.join(os.path.expanduser(\\"{target_path}\\"), \\"\\"));"'], \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        completed_process.check_returncode()
        return completed_process.stdout.rstrip()

    @classmethod
    def is_host_type(cls, identifier, configholder):

        def can_reach_remote_dir(target, target_path):
            
            completed_process = subprocess.run(['ssh', target, f'python3 -c "import os; print(os.path.exists(\\"{target_path}\\"));"'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            completed_process.check_returncode()
            return completed_process.stdout.strip() == 'True'


        if(identifier != cls.__name__.lower()):
            return False
        target = configholder.get_config_value('target')
        expanded_path = cls.expand_user_on_host(identifier, configholder.get_config_value('target_path'))
        return can_reach_remote_dir(target, expanded_path)

    @classmethod
    def add_parser(cls, subparser_container):

        default_target_path = '$HOME'

        remotehost = subparser_container.add_parser('remotehost', help='can target directories on remote hosts', allow_abbrev=False)
        remotehost.add_argument('target', help='specifies what host you wish to target, host format is the format of hostname in ssh')
        remotehost.add_argument('--target-path', metavar="path", default=default_target_path, help=f'specifies what directory on the host to target for repos (default: {default_target_path}).')

        remotehost.set_defaults(host=cls.__name__.lower())
        return remotehost

    def get_user_repo_names_and_locations(self):

        def copy_script_to_host(target, target_path, script):
            
            subprocess.run(['scp', script, f"{target}:{target_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

        def execute_script_on_host(target, script):

            completed_process = subprocess.run(['ssh', target, f"cd {target_path}; python3 {script}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            completed_process.check_returncode()
            return completed_process

        def remove_script_on_host(target, script):

            completed_process = subprocess.run(['ssh', target, f'python3 -c "import os; path = os.path.expanduser(\\"{script}\\"); os.remove(path)"'])
            completed_process.check_returncode()

        target = self.target
        target_path = self.expand_user_on_host(target, self.target_path) # target_path really is endpoint path we are looking to manipulate repos from
        remote_script_target_path = f"{target_path}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
        copy_script_to_host(target, target_path, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
        repos = execute_script_on_host(target, remote_script_target_path)
        remove_script_on_host(target, remote_script_target_path)
        repos = repos.stdout.split(',') # e.g. 'repo1,repo1 - Copy\n'
        repos[-1] = repos[-1].strip()
        for repo in repos:
            self.add_repo_name_and_location(repo, f"{target}:{target_path}{repo}")
        return self.repo_names_and_locations
