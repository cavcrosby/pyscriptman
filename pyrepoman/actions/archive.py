# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from .action import Action

class Archive(Action):

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.archive_dir = configholder.get_config_value('archive_dir')
        self.tmp_dir = 'archive_tmp'

    def run(self):

        repo_names_and_urls = self.host.get_repo_names_and_locations()
        ARCHIVE_DIR, TMP_DIR = self.archive_dir, self.tmp_dir
        super()._create_dir(ARCHIVE_DIR)
        super()._create_dir(TMP_DIR)
        super()._remove_all_dir_content(ARCHIVE_DIR)
        for repo_name in repo_names_and_urls:
            backup_repo_location = os.path.join(TMP_DIR, repo_name)
            super()._create_mirror(repo_names_and_urls[repo_name], backup_repo_location)
            super()._create_bundle(os.path.join(ARCHIVE_DIR, repo_name), backup_repo_location)
        super()._remove_dir(TMP_DIR)
