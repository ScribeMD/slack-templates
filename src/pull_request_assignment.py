"""Offer PullRequestAssignment class."""
from .slack_notification import SlackNotification


class PullRequestAssignment(SlackNotification):
    """Subclass SlackNotification for assignment of a pull request.

    Public Instance Methods:
    set_slack_message(): Set SLACK_MESSAGE env var for assigning a PR.

    Overrides:
    get_message(): Return a message assigning a pull request.
    """

    def __init__(self, token: str, assignee: str, author: str):
        """Construct a SlackNotification for assignment of a pull request.

        token: the token to use to authenticate to the GitHub API. Obtain from
        '${{ github.token }}' in the workflow.
        assignee: the GitHub user to assign the pull request to. Obtain from
        '${{ github.event.pull_request.assignee.login }}' in the workflow.
        author: the GitHub user who authored the pull request. Obtain from
        '${{ github.event.pull_request.user.login }}' in the workflow.
        """
        super().__init__(token)
        self._assignee = assignee
        self._author = author

    def get_message(self) -> str:
        """Return a message assigning a pull request."""
        actor = self.get_actor()
        if actor == self._assignee:
            assignment = "self-assigned"
        else:
            assignment = f"assigned *{self._assignee}* to"
        event_info = self.get_event_info(self._author)
        return f"{actor} {assignment} {event_info}."
