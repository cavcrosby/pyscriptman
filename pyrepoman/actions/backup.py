# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from .action import Action

class Backup(Action):

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.backup_dir = configholder.get_config_value('backup_dir')

    def run(self):

        repo_names_and_urls = self.host.get_repo_names_and_locations()
        BACKUP_DIR = self.backup_dir
        super()._create_dir(BACKUP_DIR)
        not_delete = list()
        backup_content = os.listdir(BACKUP_DIR)
        for repo_name in repo_names_and_urls:
            backup_repo_location = os.path.join(BACKUP_DIR, repo_name)
            if(not repo_name in backup_content):
                super()._create_mirror(repo_names_and_urls[repo_name], backup_repo_location)
            not_delete.append(repo_name)
        super()._remove_all_dir_content(BACKUP_DIR, not_delete)
