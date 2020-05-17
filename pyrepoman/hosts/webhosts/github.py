# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from pyrepoman.hosts.webhosts.webhost import WebHost
from util.message import Message
from util.githubauth import GitHubAuth


class GitHub(WebHost):

    HELP_DESC = "a popular web hosting for git repos"
    REPO_TYPE_CMD_ARG_NAME = "repo_type"
    REPO_OWNER_TYPE_CMD_ARG_NAME = "repo_owner_type"
    USERNAME_CMD_ARG_NAME = "username"
    OWN_CMD_ARG_NAME = "own"
    OTHER_CMD_ARG_NAME = "other"
    _REPO_TYPES_OWN = ["all", "public", "private"]
    _REPO_TYPES_OTHER = ["all", "owner", "member"]
    DEFAULT_REPO_TYPE_OWN = "all"
    DEFAULT_REPO_TYPE_OTHER = "owner"

    def __init__(self, configholder):

        super().__init__(configholder)
        self.payload = configholder.get_config_value(self.REPO_TYPE_CMD_ARG_NAME)
        self.repo_owner_type = configholder.get_config_value(
            self.REPO_OWNER_TYPE_CMD_ARG_NAME
        )
        self.username = configholder.get_config_value(self.USERNAME_CMD_ARG_NAME)

    @classmethod
    def is_host_type(cls, chosen_host):

        return chosen_host == cls._get_host_name()

    @classmethod
    def _modify_parser(cls, github_parser):

        repo_type_cmd_name_dash = cls.REPO_TYPE_CMD_ARG_NAME.replace("_", "-")

        subparser_container = github_parser.add_subparsers(
            title="[available repo-owner-types]",
            metavar="repo-owner-type [options ...]",
            dest=f"{cls.REPO_OWNER_TYPE_CMD_ARG_NAME}",
        )
        subparser_container.required = True

        own = subparser_container.add_parser(
            cls.OWN_CMD_ARG_NAME,
            help="interact with your own git repo(s)",
            allow_abbrev=False,
        )
        own.add_argument(
            f"--{repo_type_cmd_name_dash}",
            metavar="TYPE",
            default=cls.DEFAULT_REPO_TYPE_OWN,
            choices=cls._REPO_TYPES_OWN,
            help=f"specifies the type of repos to work on, choices are (default: {cls.DEFAULT_REPO_TYPE_OWN}): "
            + ", ".join(cls._REPO_TYPES_OWN),
        )

        other = subparser_container.add_parser(
            cls.OTHER_CMD_ARG_NAME,
            help="interact with another user's public git repo(s)",
            allow_abbrev=False,
        )
        other.add_argument(
            cls.USERNAME_CMD_ARG_NAME,
            help="name of user whos repos you wish to interact with",
        )
        other.add_argument(
            "--repo-type",
            metavar="TYPE",
            default=cls.DEFAULT_REPO_TYPE_OTHER,
            choices=cls._REPO_TYPES_OTHER,
            help=f"specifies the type of repos to work on, choices are (default: {cls.DEFAULT_REPO_TYPE_OTHER}): "
            + ", ".join(cls._REPO_TYPES_OTHER),
        )

        return github_parser

    def _get_user_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""
        url = (
            "https://api.github.com/user/repos"
            if self.repo_owner_type == self.OWN_CMD_ARG_NAME
            else f"https://api.github.com/users/{self.username}/repos"
        )
        try:
            auth = (
                GitHubAuth(getattr(self, "API_TOKEN"))
                if self.repo_owner_type == self.OWN_CMD_ARG_NAME
                and getattr(self, "API_TOKEN", "") != ""
                else None
            )
            response = requests.get(url, auth=auth, params={"type": self.payload})
            response.raise_for_status()
            for repo in response.json():
                super().add_repo_name_and_location(repo["name"], repo["svn_url"])
            return super().repo_names
        except (requests.exceptions.ConnectionError):
            Message.print_requests_connectionerror(self._get_host_name())
            raise
        except requests.HTTPError:
            Message.print_requests_httperror(self._get_host_name(), response)
            raise
