"""Offer get_slack_notification function for use of package via CLI."""

from collections.abc import Sequence

from .custom_notification import CustomNotification
from .pull_request_assignment import PullRequestAssignment
from .reviewers_assignment import ReviewersAssignment
from .slack_notification import SlackNotification
from .workflow_result import WorkflowResult


def get_slack_notification(arguments: Sequence[str]) -> SlackNotification:
    """Return an appropriately configured SlackNotification.

    arguments: the command-line arguments passed to set_slack_message.py. Do not include
    the first element of sys.argv since this is merely the name of the Python script
    itself.
    """
    template, results, message, token, author, reviewers, assignee = arguments
    if template == "result":
        return WorkflowResult(token, results.split())
    if template == "reviewers":
        return ReviewersAssignment(token, reviewers, author)
    if template == "assignee":
        return PullRequestAssignment(token, assignee, author)
    if template == "custom":
        return CustomNotification(token, message)
    return CustomNotification(
        token,
        "Unrecognized template passed to slack-templates: template. Valid options are "
        '"result," "reviewers," "assignee," or "custom."',
    )
