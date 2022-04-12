"""Offer ReviewersAssignment class."""
from .slack_notification import SlackNotification


class ReviewersAssignment(SlackNotification):
    """Subclass SlackNotification for assignment of code reviewers.

    Public Instance Methods:
    set_slack_message(): Set SLACK_MESSAGE env var for assigning reviewers.

    Overrides:
    get_message(): Return a message assigning reviewers for a pull request.
    """

    def __init__(self, token: str, reviewers: str, author: str):
        """Construct a SlackNotification for assignment of code reviewers.

        token: the token to use to authenticate to the GitHub API. Obtain from
        '${{ github.token }}' in the workflow.
        reviewers: the GitHub users to request reviews from. Obtain from
        "*${{ join(github.event.pull_request.requested_reviewers.*.login, '*, *') }}*"
        in the workflow.
        author: the GitHub user who authored the pull request. Obtain from
        '${{ github.event.pull_request.user.login }}' in the workflow.
        """
        super().__init__(token)
        self._reviewers = reviewers
        self._author = author

    def get_message(self) -> str:
        """Return a message requesting review of a pull request."""
        actor = self.get_actor()
        request = (
            "self-requests review"
            if f"*{actor}*" == self._reviewers
            else f"requests review from {self._reviewers}"
        )
        event_info = self.get_event_info(self._author)
        return f"{actor} {request} of {event_info}."
