"""The 'GitHub' host class module."""
# Standard Library Imports

# Third Party Imports
import requests
import toml

# Local Application Imports
from pyrepoman.hosts.webhosts.webhost import WebHost
from pyrepoman.pyrepoman_variables import REQUIRE_SUBCOMMANDS
from util.message import Message
from util.githubauth import GitHubAuth


class GitHub(WebHost):
    """The 'GitHub' host class.

    This interface allows you to interact
    with Git repos from github.com.

    Parameters
    ----------
    configholder : util.configholder.ConfigHolder
        An instantiation of ConfigHolder, used to hold program configurations.

    Attributes
    ----------
    HELP_DESC : str
        Parser description of GitHub
        when using -h/--help (see Examples).
    REPO_TYPE_CMD_ARG_NAME : str
        The name of repo type optional argument for both
        GitHub subcommands.
    REPO_OWNER_TYPE_CMD_ARG_NAME : str
        Argument name for type of github.com git repo.
    USERNAME_CMD_ARG_NAME : str
        Username argument for the other subcommand.
    OWN_CMD_ARG_NAME : str
        Subcommand name for a subcommand in GitHub.
    OTHER_CMD_ARG_NAME : str
        Subcommand name for a subcommand in GitHub.
    DEFAULT_REPO_TYPE_OWN : str
        When using the subcommand `OWN_CMD_ARG_NAME`
        this is the default option when no option is
        selected by the user.
    DEFAULT_REPO_TYPE_OTHER : str
        When using the subcommand `OTHER_CMD_ARG_NAME`
        this is the default option when no option is
        selected by the user.

    """

    HELP_DESC = "a popular web hosting for git repos"
    REPO_TYPE_CMD_ARG_NAME = "repo_type"
    REPO_OWNER_TYPE_CMD_ARG_NAME = "repo_owner_type"
    USERNAME_CMD_ARG_NAME = "username"
    OWN_CMD_ARG_NAME = "own"
    OTHER_CMD_ARG_NAME = "other"
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
        """How the host type is determined.
        
        Parameters
        ----------
        chosen_host : str
            Input received from the command line.
            
        Returns
        -------
        bool
            Whether or not the user has chosen this host type
            and that other requirements were also met for
            it to be this host type.

        Examples
        --------
        (pyrepoman) reap2sow1@Ron:~$ pyrepoman fetch -h # TODO FINALIZE EXAMPLE
        available hosts:
            host [options ...]
                [...]
                github         a popular web hosting for git repos

        """
        return chosen_host == cls._get_host_name()

    @classmethod
    def _modify_parser(cls, github_parser):
        """Allows the github parser to take custom arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        Returns
        -------
        parser : argparse.ArgumentParser
            A normal argparse.ArgumentParser parser that
            can additional positional/optional arguments.

        """
        repo_types_own = ["all", "public", "private"]
        repo_types_other = ["all", "owner", "member"]

        repo_type_cmd_name_dash = cls.REPO_TYPE_CMD_ARG_NAME.replace("_", "-")

        subparser_container = github_parser.add_subparsers(
            title="available repo-owner-types",
            metavar="repo-owner-type [options ...]",
            dest=f"{cls.REPO_OWNER_TYPE_CMD_ARG_NAME}",
        )
        subparser_container.required = REQUIRE_SUBCOMMANDS

        own = subparser_container.add_parser(
            cls.OWN_CMD_ARG_NAME,
            help="interact with your own git repo(s)",
            allow_abbrev=False,
        )
        own.add_argument(
            f"--{repo_type_cmd_name_dash}",
            metavar="TYPE",
            default=cls.DEFAULT_REPO_TYPE_OWN,
            choices=repo_types_own,
            help=f"specifies the type of repos to work on, choices are (default: {cls.DEFAULT_REPO_TYPE_OWN}): "
            + ", ".join(repo_types_own),
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
            f"--{repo_type_cmd_name_dash}",
            metavar="TYPE",
            default=cls.DEFAULT_REPO_TYPE_OTHER,
            choices=repo_types_other,
            help=f"specifies the type of repos to work on, choices are (default: {cls.DEFAULT_REPO_TYPE_OTHER}): "
            + ", ".join(repo_types_other),
        )

        return github_parser

    def _get_user_repo_names_and_locations(self):
        """Used to determine repo names and locations for github.
        
        This method is the 'how' in getting
        the repo names and locations. Host
        object will store the locations of
        the repos.

        Currently, this function uses github.com's
        RESTv3 API.

        Returns
        -------
        repo_names : list of str
            Git repo names are returned in a list.

        """
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
