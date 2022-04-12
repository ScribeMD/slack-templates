"""Offer CustomNotification class."""
from dataclasses import dataclass

from .slack_notification import SlackNotification


@dataclass
class CustomNotification(SlackNotification):
    """Subclass SlackNotification for custom notifications.

    Public Instance Methods:
    set_slack_message(): Set SLACK_MESSAGE env var for custom notification.

    Overrides:
    get_message(): Return the message passed to the constructor.
    """

    _message: str

    def __init__(self, token: str, message: str):
        """Construct a SlackNotification for custom notification.

        token: the token to use to authenticate to the GitHub API. Obtain from
        '${{ github.token }}' in the workflow.
        message: the string to use as the value of SLACK_MESSAGE.
        """
        super().__init__(token)
        self._message = message

    def get_message(self) -> str:
        """Return the message that was passed to the constructor."""
        return self._message
