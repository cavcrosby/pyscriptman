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

    @classmethod
    def add_parser(cls, subparser_container):

        subcommand = cls.__name__.lower()
        archive = subparser_container.add_parser(subcommand, help='archive all Git repos, done by bundling repos', allow_abbrev=False)
        archive.add_argument('dest', help='where to store archives (destination)')
        archive.set_defaults(action=subcommand)
        return archive

    def run(self):

        repo_names_and_locations = self.host.get_user_repo_names_and_locations()
        dest, tmp_dir = self.dest, self.tmp_dir
        super()._create_dir(dest)
        super()._create_dir(tmp_dir)
        super()._remove_all_dir_content(dest)
        for repo_name in repo_names_and_locations:
            backup_repo_location = os.path.join(tmp_dir, repo_name)
            super()._create_mirror(self.host.get_location_from_repo_name(repo_name), backup_repo_location)
            super()._create_bundle(os.path.join(dest, repo_name), backup_repo_location)
        super()._remove_dir(tmp_dir)
