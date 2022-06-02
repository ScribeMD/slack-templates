"""Offer SlackNotification abstract base class."""
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from json import dumps, load
from os import environ
from os.path import dirname, join
from re import fullmatch
from sys import stderr
from typing import Any, Optional, Union, cast
from urllib.error import URLError
from urllib.request import Request, urlopen

JsonValue = Union[None, bool, int, float, str, Sequence[Any], Mapping[str, Any]]
JsonObject = Mapping[str, JsonValue]


def _get_json_value(obj: JsonObject, path: Sequence[str]) -> JsonValue:
    """Return the value at the given path in the given JSON object.

    Return the object itself if the path is empty. Raise TypeError if the object is not
    valid JSON, but only check along the specified path for performance.
    """
    if not path:
        return obj

    for i, key in enumerate(path[:-1]):
        value = obj.get(key)
        if not isinstance(value, dict):
            current_path = ".".join(path[: i + 1])
            raise TypeError(
                f"Expected JSON object to have an object at {current_path}; got:\n"
                f"{obj}"
            )
        obj = cast(JsonObject, value)
    value = obj.get(path[-1])

    if not isinstance(value, (type(None), bool, int, float, str, list, dict)):
        raise TypeError(f"Expected JSON object to have {'.'.join(path)}; got:\n{obj}")
    return value


class SlackNotification(ABC):
    """Offer utilities for issuing Slack notifications from GitHub Actions.

    Abstract Methods:
    get_message(): Called by set_slack_message() to get the message to be set.

    Public Methods:
    set_slack_message(): Set SLACK_MESSAGE env var to self.get_message().
    get_actor(): Return the GitHub user that triggered this workflow.
    get_workflow_link(): Return a Slack link to this workflow.
    get_event_info(author=None): Return Slack copy for the triggering event.
    """

    _GRAPHQL_QUERY_PATH = join(
        dirname(__file__), "pull_request_for_base_branch_oid.graphql"
    )
    """Contains a GraphQL query that gets the pull request associated with a commit."""

    def __init__(self, token: str, pr_number: Optional[int] = None):
        """Store the given token and some GitHub environment variables.

        token: the token to use to authenticate to the GitHub API. Obtain from
        '${{ github.token }}' in the workflow.
        pr_number: the pull request number if applicable. Obtain from
        '${{ github.event.pull_request.number }}' in the workflow.
        """
        self._headers = {
            "Accept": "application/vnd.github.v4.json",
            "Authorization": f"Bearer {token}",
        }
        self._pr_number = pr_number
        self._actor = environ["GITHUB_ACTOR"]

        server_url = environ["GITHUB_SERVER_URL"]
        self._repository = environ["GITHUB_REPOSITORY"]
        self._repository_url = f"{server_url}/{self._repository}"

        self._event_name = environ["GITHUB_EVENT_NAME"]
        self._sha = environ["GITHUB_SHA"]

    def set_slack_message(self) -> None:
        """Add environment variable SLACK_MESSAGE to GitHub Actions env.

        Each step in a workflow is run in a separate shell, so append the Bash command
        to set SLACK_MESSAGE to the appropriate shell config file. The message is
        obtained from self.get_message(), which must be overridden.
        """
        github_env = environ["GITHUB_ENV"]
        with open(github_env, "a", encoding="utf-8") as env_file:
            env_file.write(f"SLACK_MESSAGE={self.get_message()}\n")

    @abstractmethod
    def get_message(self) -> str:
        """Return the message to be set by set_slack_message()."""

    def get_actor(self) -> str:
        """Return the GitHub user that triggered this workflow."""
        return self._actor

    def get_workflow_link(self) -> str:
        """Return a Slack link to this workflow's GitHub Actions page."""
        run_id = environ["GITHUB_RUN_ID"]
        workflow_url = f"{self._repository_url}/actions/runs/{run_id}"
        workflow_name = environ["GITHUB_WORKFLOW"]
        return f"<{workflow_url}|{workflow_name} workflow>"

    def get_event_info(self, author: Optional[str] = None) -> str:
        """Return detailed Slack notification copy for the current event.

        Include Slack links to the associated branch and repository as well as one
        specific to the type of GitHub Actions event that triggered this workflow.

        author: the author of the pull request, which is included if it differs from the
        actor, meaning the user that triggered the workflow
        """
        branch = self._get_branch()
        event_info = self._get_event_link()
        branch_url = f"{self._repository_url}/commits/{branch}"
        branch_link = f"<{branch_url}|{branch}>"
        repository_link = f"<{self._repository_url}|{self._repository}>"
        event_info = f"{event_info} {branch_link} on {repository_link}"
        if author and self._actor != author:
            event_info += f" by {author}"
        return event_info

    def _get_branch(self) -> str:
        """Return the branch associated with the current GitHub Actions event.

        For pull_request events, return the head (a.k.a., from) branch, not the base
        (a.k.a., to) branch. For push events, return the branch that was pushed to.
        """
        return (
            environ["GITHUB_HEAD_REF"]
            if self._event_name == "pull_request"
            else environ["GITHUB_REF_NAME"]
        )

    def _get_event_link(self) -> str:
        """Return a Slack link appropriate to the current GitHub Actions event.

        Only pull_request and push events are supported. For all other events, link to
        GitHub's documentation for the unexpected event.
        """
        if self._event_name == "pull_request":
            return self._get_pull_link()

        if self._event_name == "push":
            return self._get_push_link()

        event_url = (
            "https://docs.github.com/en/actions/reference/events-that-trigger-workflows"
            + f"#{self._event_name}"
        )
        return f"unexpected <{event_url}|{self._event_name}> event"

    def _get_pull_link(self) -> str:
        """Return a Slack link to the pull request for a pull_request event."""
        event_url = f"{self._repository_url}/pull/{self._pr_number}"
        return f"<{event_url}|#{self._pr_number}> from"

    def _get_push_link(self) -> str:
        """Return a Slack link to the pull request for a push event.

        If the associated pull request cannot be determined, link to the pushed head
        commit instead.
        """
        pr_number = self._get_associated_pr_number()
        if pr_number is None:
            event_url = f"{self._repository_url}/commit/{self._sha}"
            return f"push of <{event_url}|{self._sha}> to"

        event_url = f"{self._repository_url}/pull/{pr_number}"
        return f"merge of <{event_url}|#{pr_number}> to"

    def _get_associated_pr_number(self) -> Optional[int]:
        """Return the number of the merged pull request for the pushed commit.

        This is the pull request that introduced the pushed commit to the branch. Return
        None if the pull request number can not be determined (e.g., because the commit
        hasn't been merged to the default branch or the network failed). Raise a
        TypeError if the response is malformed.
        """
        if self._pr_number is not None:
            return self._pr_number

        pattern = r"([^/]+)/([^/]+)"
        if not (match := fullmatch(pattern, self._repository)):
            raise ValueError(
                f'Expected $GITHUB_REPOSITORY to match "{pattern}"; got: '
                f"{self._repository}"
            )

        with open(self._GRAPHQL_QUERY_PATH, encoding="utf-8") as input_stream:
            query_string = input_stream.read()

        query: JsonObject = {
            "query": query_string,
            "variables": {
                "owner": match.group(1),
                "repo": match.group(2),
                "oid": self._sha,
            },
        }

        self._pr_number = (
            self._validate_pr_num(response)
            if (response := self._graphql_request(query))
            else None
        )
        return self._pr_number

    def _graphql_request(self, body: JsonObject) -> Optional[JsonObject]:
        """Return the parsed JSON response for a GitHub GraphQL request.

        Return None if the request fails. Raise a ValueError if the response contains
        GraphQL errors.

        body: the GitHub GraphQL request body
        """
        url = environ["GITHUB_GRAPHQL_URL"]
        json_string = dumps(body)
        request_data = json_string.encode()
        request = Request(url, data=request_data, headers=self._headers)
        try:
            # This is only unsafe when $GITHUB_GRAPHQL_URL is not trusted.
            with urlopen(request) as response:  # nosec
                response_body = load(response)
        except URLError as url_error:
            print(url_error, file=stderr)
            return None

        if not isinstance(response_body, dict):
            raise TypeError(f"Expected JSON response; got:\n{response_body}")

        if graphql_errors := response_body.get("errors"):
            raise ValueError(graphql_errors)

        return cast(JsonObject, response_body)

    def _validate_pr_num(self, response: JsonObject) -> Optional[int]:
        """Return the pull request number contained in the given response.

        Return None if the response isn't for a commit merged to the default branch.
        Raise a TypeError if the response is malformed.

        response: the GitHub GraphQL response to the _PULL_REQUEST_FOR_BASE_BRANCH_OID
        query, which gets: "the merged Pull Request that introduced the commit to the
        repository. If the commit is not present in the default branch, additionally
        returns open Pull Requests associated with the commit."
        ~ https://docs.github.com/en/graphql/reference/objects#commit
        """
        prs_path = ("data", "repository", "object", "associatedPullRequests")
        pull_requests = _get_json_value(response, prs_path)
        if not isinstance(pull_requests, dict):
            raise TypeError(
                f"Expected GraphQL response to {self._GRAPHQL_QUERY_PATH} to have an "
                f"object at {'.'.join(prs_path)}; got:\n{response}"
            )

        nodes = pull_requests.get("nodes")
        if not isinstance(nodes, list):
            raise TypeError(
                f"Expected GraphQL response to {self._GRAPHQL_QUERY_PATH} to have an "
                f"array at {'.'.join(prs_path)}.nodes; got:\n{response}"
            )
        if pull_requests.get("totalCount") != 1 or len(nodes) != 1:
            return None

        node = nodes[0]
        if not isinstance(node, dict):
            raise TypeError(
                f"Expected GraphQL response to {self._GRAPHQL_QUERY_PATH} to have an "
                f"object at {'.'.join(prs_path)}.nodes[0]; got:\n{response}"
            )

        oid = _get_json_value(node, ("mergeCommit", "oid"))
        if not isinstance(oid, str):
            raise TypeError(
                f"Expected GraphQL response to {self._GRAPHQL_QUERY_PATH} to have a "
                f"string at {'.'.join(prs_path)}.nodes[0].mergeCommit.oid; got:\n"
                f"{response}"
            )
        if oid != self._sha:
            return None

        pr_number = node.get("number")
        if not isinstance(pr_number, int):
            raise TypeError(
                f"Expected GraphQL response to {self._GRAPHQL_QUERY_PATH} to have an "
                f"integer at {'.'.join(prs_path)}.nodes[0].number; got:\n{response}"
            )
        return pr_number
