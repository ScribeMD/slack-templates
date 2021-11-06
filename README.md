# slack-templates

[![Test](https://github.com/ScribeMD/slack-templates/workflows/Test/badge.svg)](https://github.com/ScribeMD/slack-templates/actions/workflows/test.yaml)
[![Bump Version](https://github.com/ScribeMD/slack-templates/workflows/Bump%20Version/badge.svg)](https://github.com/ScribeMD/slack-templates/actions/workflows/bump-version.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Send Informative, Concise Slack Notifications With Minimal Effort

<!--TOC-->

- [slack-templates](#slack-templates)
  - [Slack Integration](#slack-integration)
  - [Available Templates](#available-templates)
  - [Usage](#usage)
    - [Report the status of the current job](#report-the-status-of-the-current-job)
    - [Summarize the results of an entire workflow](#summarize-the-results-of-an-entire-workflow)
    - [Report a custom result](#report-a-custom-result)
    - [Notify reviewers of a pull request](#notify-reviewers-of-a-pull-request)
    - [Notify assignee of a pull request](#notify-assignee-of-a-pull-request)
    - [Send a custom notification](#send-a-custom-notification)
  - [Relation to slack-send](#relation-to-slack-send)
  - [Bug Reports](#bug-reports)
  - [Contributing](#contributing)
  - [Changelog](#changelog)

<!--TOC-->

## Slack Integration

- Create a custom Slack app with the chat:write scope.
- Install the app to your workspace, and copy the provided OAuth access token.
- Create a GitHub secret to store the bot token.
- Invite your bot to the desired channel.
- Secondary-click on the channel, and select "Copy link."
- Create a GitHub secret to store the final portion of the path. The channel ID
  is neither the name of the channel nor the URL.

## Available Templates

The `template` parameter controls the structure of the Slack notification. Here
are all currently supported templates:

- `"result"`:
  - `pull_request` event: \<workflow> **\<result>** for \<PR #> from
    \<branch> on \<repository> by \<username>.
  - `push` event:
    - merge of pull request: \<workflow> **\<result>** for merge of \<PR #> to
      \<branch> on \<repository> by \<username>.
    - direct push of branch: \<workflow> **\<result>** for push of \<sha> to
      \<branch> on \<repository> by \<username>.
- `"reviewers"`:
  - `requestor != requestee`: \<requestor> requests review from **\<reviewers>**
    of \<PR #> from \<branch> on \<repository>.
  - `requestor == requestee`: \<username> self-requests review of \<PR #> from
    \<branch> on \<repository>.
- `"assignee"`:
  - `assignor != assignee`: \<assignor> assigned **\<assignee>** \<PR #> from
    \<branch> on \<repository>.
  - `assignor == assignee`: \<username> self-assigned \<PR #> from \<branch>
    on \<repository>.
- `"custom"`: Pass your custom message via the `message` parameter.

All usernames refer to GitHub usernames. Users with differing Slack and GitHub
usernames may wish to register their GitHub username for
[Slack keyword notifications](https://slack.com/slack-tips/get-notified-when-someone-mentions-a-topic-you-care-about).
Workflow names, pull request numbers, commit shas, branches, and repositories
all link to the pertinent GitHub page. If you would like to see a template
added, please open an issue or better still a pull request.

Reliably determining the pull request associated with a `push` event requires
read permissions on the `contents` scope. Even the restrictive defaults grant
this permission. If permissions are granted explicitly and `contents: read`
is excluded, the commit sha will be reported instead of the pull request number,
because merges will be indistinguishable from direct pushes.

## Usage

### Report the status of the current job

- Add the following step to the bottom of the job:

```yaml
- name: Send Slack notification with job status.
  if: always()
  uses: ScribeMD/slack-templates@0
  with:
    bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
    channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
    template: result
```

### Summarize the results of an entire workflow

- Create a new job at the end of the workflow that depends on (a.k.a., "needs")
  all other jobs but always runs.
- Pass `"${{ join(needs.*.result, ' ') }}"` as the `results`.

The result of the entire workflow is the highest ranking of all results given.
The ranking is as follows:

1. failure
1. cancelled
1. success
1. skipped

```yaml
name: My Workflow
on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main
jobs:
  job1: ...
  job2: ...
  job3: ...
  notify:
    if: always()
    needs:
      - job1
      - job2
      - job3
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack notification with workflow result.
        uses: ScribeMD/slack-templates@0
        with:
          bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
          channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
          template: result
          results: "${{ join(needs.*.result, ' ') }}"
```

### Report a custom result

- Determine what result to send in preceding steps.
- Report the result at the bottom of the job as before.
- Take care to quote `results` for use as a Bash command line argument.

```yaml
- name: Detect third-party network outage.
  id: network
  run: |
    ...
    echo "::set-output name=outage::$OUTAGE"
  shell: bash
- name: Send Slack notification with custom result.
  if: always() && steps.network.outputs.outage == 'true'
  uses: ScribeMD/slack-templates@0
  with:
    bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
    channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
    template: result
    results: '"failure caused by third-party network outage"'
```

### Notify reviewers of a pull request

```yaml
name: Notify Reviewers
on:
  pull_request:
    types:
      - review_requested
jobs:
  notify-reviewers:
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack notification requesting code review.
        uses: ScribeMD/slack-template@0
        with:
          bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
          channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
          template: reviewers
```

### Notify assignee of a pull request

```yaml
name: Notify Assignee
on:
  pull_request:
    types:
      - assigned
jobs:
  notify-assignee:
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack notification assigning pull request.
        uses: ScribeMD/slack-templates@0
        with:
          bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
          channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
          template: assignee
```

### Send a custom notification

```yaml
- name: Send custom Slack notification.
  if: always()
  uses: ScribeMD/slack-templates@0
  with:
    bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
    channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
    message: "${{ github.actor }} requests approval to run workflow."
```

## Relation to slack-send

This action wraps [slack-send](https://github.com/slackapi/slack-github-action),
its only runtime dependency, inheriting slack-send's support for all
[GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources).
There are three principal differences between these actions:

- slack-templates offers some default messages; slack-send presently does not.
- slack-send supports Slack's Workflow Builder (unavailable on free Slack plan)
  in addition to Slack apps. slack-templates only supports Slack apps.
- slack-send accepts the bot token as environment variable `SLACK_BOT_TOKEN`.
  slack-templates accepts it as the input parameter `bot-token`.

## Bug Reports

If you are not receiving notifications, please review
[the Slack Integration section](#slack-integration) and then file a bug report
containing the GitHub Action's logs if that doesn't resolve your issue. If you
are receiving nondescript Slack notifications, please file a bug report with the
notification you received taking care to preserve the links.

## Contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

Please refer to [CHANGELOG.md](CHANGELOG.md).
