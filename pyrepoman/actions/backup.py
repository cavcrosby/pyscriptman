# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from .action import Action

class Backup(Action):

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.dest = configholder.get_config_value('dest')

    @classmethod
    def add_parser(cls, subparser_container):

        parser_backup = subparser_container.add_parser('backup', help='backup all Git repos, done by mirroring repos fully', allow_abbrev=False)
        parser_backup.add_argument('dest', help='where to store backups (destination)')
        parser_backup.set_defaults(action='backup')
        return parser_backup

    def run(self):

        repo_names_and_locations = self.host.get_repo_names_and_locations()
        DEST = self.dest
        super()._create_dir(DEST)
        not_delete = list()
        backup_content = os.listdir(DEST)
        for repo_name in repo_names_and_locations:
            backup_repo_location = os.path.join(DEST, repo_name)
            if(not repo_name in backup_content):
                super()._create_mirror(self.host.get_location_from_repo_name(repo_name), backup_repo_location)
            not_delete.append(repo_name)
        super()._remove_all_dir_content(DEST, not_delete)
