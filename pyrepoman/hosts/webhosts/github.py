# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from .webhost import WebHost

class GitHub(WebHost):

    def __init__(self, configholder):

        super().__init__(configholder)
        self.payload = configholder.get_config_value('repo_type')
        self.repo_owner_type = configholder.get_config_value('repo_owner_type')
        self.username = configholder.get_config_value('username')

    @classmethod
    def is_host_type(cls, identifier, configholder):

        if(identifier == cls.__name__.lower()):
            return True

        return False

    @classmethod
    def add_parser(cls, subparser_container):

        REPO_TYPES_OWN = ['all', 'public', 'private']
        DEFAULT_OWN = 'all'
        REPO_TYPES_OTHER = ['all', 'owner', 'member']
        DEFAULT_OTHER = 'owner'

        parser_github = subparser_container.add_parser('github', help='a popular web hosting for git repos', allow_abbrev=False)
        subparser_github_container = parser_github.add_subparsers(title='available repo-owner-types', metavar='repo-owner-type [options ...]', dest='repo_owner_type')
        subparser_github_container.required = True
        subparser_github_own = subparser_github_container.add_parser('own', help='interact with your own git repo(s)', allow_abbrev=False)
        subparser_github_own.add_argument('--repo-type', metavar="TYPE", default=DEFAULT_OWN, choices=REPO_TYPES_OWN, help=f'specifies the type of repos to work on, choices are (default: {DEFAULT_OWN}): ' + ', '.join(REPO_TYPES_OWN))
        subparser_github_other = subparser_github_container.add_parser('other', help="interact with another user's public git repo(s)", allow_abbrev=False)
        subparser_github_other.add_argument('username', help='name of user whos repos you wish to interact with')
        subparser_github_other.add_argument('--repo-type', metavar="TYPE", default=DEFAULT_OTHER, choices=REPO_TYPES_OTHER, help=f'specifies the type of repos to work on, choices are (default: {DEFAULT_OTHER}): ' + ', '.join(REPO_TYPES_OTHER))
        parser_github.set_defaults(host='github')
        return parser_github

    def _get_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""
        try:
            if(self.repo_owner_type == 'own'):
                repos = requests.get("https://api.github.com/user/repos", auth=(getattr(self, 'user'), getattr(self, 'api_token')), params={"type": self.payload})
            else:
                repos = requests.get(f"https://api.github.com/users/{self.username}/repos", params={"type": self.payload})
            repos.raise_for_status()
            for repo in repos.json():
                self.add_repo_name_and_location(repo['name'], repo['svn_url'])
            return self.repo_names_and_locations
        except ConnectionError:
            print("Error: could not connect to GitHub, check network settings or try again later")
            raise SystemExit()
        except requests.HTTPError:
            print(f"Error: communicating with GitHub failed; Reason: {repos.json()['message']}")
            raise SystemExit()
