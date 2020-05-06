# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from pyrepoman.hosts.webhosts.webhost import WebHost
from util.printexception import PrintException
from util.githubauth import GitHubAuth


class GitHub(WebHost):

    HELP_DESC = "a popular web hosting for git repos"

    def __init__(self, configholder):

        super().__init__(configholder)
        self.payload = configholder.get_config_value("repo_type")
        self.repo_owner_type = configholder.get_config_value("repo_owner_type")
        self.username = configholder.get_config_value("username")

    @classmethod
    def is_host_type(cls, chosen_host):

        return chosen_host == cls._get_host_name()

    @classmethod
    def _modify_parser(cls, parser):

        repo_types_own = ["all", "public", "private"]
        default_own = "all"
        repo_types_other = ["all", "owner", "member"]
        default_other = "owner"

        subparser_github_container = parser.add_subparsers(
            title="available repo-owner-types",
            metavar="repo-owner-type [options ...]",
            dest="repo_owner_type",
        )
        subparser_github_container.required = True

        own = subparser_github_container.add_parser(
            "own", help="interact with your own git repo(s)", allow_abbrev=False
        )
        own.add_argument(
            "--repo-type",
            metavar="TYPE",
            default=default_own,
            choices=repo_types_own,
            help=f"specifies the type of repos to work on, choices are (default: {default_own}): "
            + ", ".join(repo_types_own),
        )

        other = subparser_github_container.add_parser(
            "other",
            help="interact with another user's public git repo(s)",
            allow_abbrev=False,
        )
        other.add_argument(
            "username", help="name of user whos repos you wish to interact with"
        )
        other.add_argument(
            "--repo-type",
            metavar="TYPE",
            default=default_other,
            choices=repo_types_other,
            help=f"specifies the type of repos to work on, choices are (default: {default_other}): "
            + ", ".join(repo_types_other),
        )

        return parser

    def _get_user_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""
        url = (
            "https://api.github.com/user/repos"
            if self.repo_owner_type == "own"
            else f"https://api.github.com/users/{self.username}/repos"
        )
        try:
            auth = (
                GitHubAuth(getattr(self, "api_token"))
                if self.repo_owner_type == "own"
                else None
            )
            response = requests.get(url, auth=auth, params={"type": self.payload})
            response.raise_for_status()
            for repo in response.json():
                self.add_repo_name_and_location(repo["name"], repo["svn_url"])
            return self.repo_names_and_locations
        except AttributeError as e:
            PrintException.print_attribute_error(e)
            raise
        except (requests.exceptions.ConnectionError):
            PrintException.print_requests_connectionerror(self._get_host_name())
            raise
        except requests.HTTPError:
            PrintException.print_requests_httperror(self._get_host_name(), response)
            raise
