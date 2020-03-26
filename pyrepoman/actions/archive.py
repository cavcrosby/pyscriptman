# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from .action import Action

class Archive(Action):

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.dest = configholder.get_config_value('dest')
        self.tmp_dir = 'archive_tmp'

    def run(self):

        repo_names_and_urls = self.host.get_repo_names_and_locations()
        DEST, TMP_DIR = self.dest, self.tmp_dir
        super()._create_dir(DEST)
        super()._create_dir(TMP_DIR)
        super()._remove_all_dir_content(DEST)
        for repo_name in repo_names_and_urls:
            backup_repo_location = os.path.join(TMP_DIR, repo_name)
            super()._create_mirror(repo_names_and_urls[repo_name], backup_repo_location)
            super()._create_bundle(os.path.join(DEST, repo_name), backup_repo_location)
        super()._remove_dir(TMP_DIR)
