#!/usr/bin/env python3

"""Set Slack message for GitHub Action.

Usage: python set_slack_message.py \
    <template> <results> <message> <token> <author> <reviewers> <assignee>
"""
import sys

from src.cli import get_slack_notification

slack_notification = get_slack_notification(sys.argv[1:])
slack_notification.set_slack_message()
