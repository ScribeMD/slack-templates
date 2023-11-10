#!/usr/bin/env python3
"""Set Slack message for GitHub Action.

Usage: python set_slack_message.py \
    <template> <results> <message> <token> <author> <reviewers> <assignee> <pr_number>
"""
from sys import argv

from src.cli import get_slack_notification

SLACK_NOTIFICATION = get_slack_notification(argv[1:])
SLACK_NOTIFICATION.set_slack_message()
