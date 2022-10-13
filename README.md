# slack-templates

[![GitHub Action: Try Me](https://img.shields.io/badge/GitHub_Action-Try_Me-AC80A0?logo=githubactions&logoColor=2088FF&labelColor=343B42)](https://github.com/marketplace/actions/slack-templates)
[![Slack Templates](https://img.shields.io/badge/Slack-Templates-755C1B?logo=slack&logoColor=4A154B&labelColor=343B42)](https://slack.com/integrations)
[![Test Workflow Status](https://github.com/ScribeMD/slack-templates/workflows/Test/badge.svg)](https://github.com/ScribeMD/slack-templates/actions/workflows/test.yaml)
[![Copy/Paste: 0%](https://img.shields.io/badge/Copy%2FPaste-0%25-B200B2?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik03LjAyNCAzLjc1YzAtLjk2Ni43ODQtMS43NSAxLjc1LTEuNzVIMjAuMjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXYxMS40OThhMS43NSAxLjc1IDAgMDEtMS43NSAxLjc1SDguNzc0YTEuNzUgMS43NSAwIDAxLTEuNzUtMS43NVYzLjc1em0xLjc1LS4yNWEuMjUuMjUgMCAwMC0uMjUuMjV2MTEuNDk4YzAgLjEzOS4xMTIuMjUuMjUuMjVIMjAuMjVhLjI1LjI1IDAgMDAuMjUtLjI1VjMuNzVhLjI1LjI1IDAgMDAtLjI1LS4yNUg4Ljc3NHoiLz48cGF0aCBkPSJNMS45OTUgMTAuNzQ5YTEuNzUgMS43NSAwIDAxMS43NS0xLjc1MUg1LjI1YS43NS43NSAwIDExMCAxLjVIMy43NDVhLjI1LjI1IDAgMDAtLjI1LjI1TDMuNSAyMC4yNWMwIC4xMzguMTExLjI1LjI1LjI1aDkuNWEuMjUuMjUgMCAwMC4yNS0uMjV2LTEuNTFhLjc1Ljc1IDAgMTExLjUgMHYxLjUxQTEuNzUgMS43NSAwIDAxMTMuMjUgMjJoLTkuNUExLjc1IDEuNzUgMCAwMTIgMjAuMjVsLS4wMDUtOS41MDF6Ii8+PC9zdmc+&labelColor=343B42)](https://github.com/kucherenko/jscpd)

[![Automated Updates: Dependabot](https://img.shields.io/badge/Dependabot-Automated_Updates-3CBBB1?logo=dependabot&logoColor=025E8C&labelColor=666)](https://github.com/dependabot)
[![Language: Python](https://img.shields.io/badge/Python-Language-A42CD6?logo=python&logoColor=3776AB&labelColor=666)](https://www.python.org/)
[![Package Management: Poetry](https://img.shields.io/badge/Poetry-Package_Management-06BA63?logo=poetry&logoColor=60A5FA&labelColor=666)](https://python-poetry.org/)
[![Git Hooks: pre-commit](https://img.shields.io/badge/pre--commit-Git_Hooks-04E762?logo=precommit&logoColor=FAB040&labelColor=666)](https://pre-commit.com/)
[![Commit Style: Conventional Commits](https://img.shields.io/badge/Conventional_Commits-Commit_Style-090C9B?logo=conventionalcommits&logoColor=FE5196&labelColor=666)](https://conventionalcommits.org)
[![Releases: Semantic Versioning](https://img.shields.io/badge/SemVer-Releases-08A045?logo=semver&logoColor=3F4551&labelColor=666)](https://semver.org/)
[![Code Style: Prettier](https://img.shields.io/badge/Prettier-Code_Style-000?logo=prettier&logoColor=F7B93E&labelColor=666)](https://prettier.io/)
[![Code Style: Black](https://img.shields.io/badge/Black-Code_Style-000?labelColor=666)](https://github.com/psf/black)
[![Code Style: EditorConfig](https://img.shields.io/badge/EditorConfig-Code_Style-FF69EB?logo=editorconfig&logoColor=FEFEFE&labelColor=666)](https://editorconfig.org/)
[![Imports: isort](https://img.shields.io/badge/isort-Imports-1674B1?labelColor=666)](https://pycqa.github.io/isort/)
[![Security: Bandit](https://img.shields.io/badge/Bandit-Security-yellow?labelColor=666)](https://github.com/PyCQA/bandit)
[![Editor: Visual Studio Code](https://img.shields.io/badge/VSCode-Editor-EE8434?logo=visualstudiocode&logoColor=007ACC&labelColor=666)](https://code.visualstudio.com/)

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
  - [Inputs](#inputs)
    - [Required](#required)
    - [Optional](#optional)
  - [Relation to slack-send](#relation-to-slack-send)
  - [Bug Reports](#bug-reports)
  - [Permissions](#permissions)
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
    uses: ScribeMD/slack-templates@0.6.11
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
        uses: ScribeMD/slack-templates@0.6.11
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
    echo "OUTAGE=$OUTAGE" >>"$GITHUB_OUTPUT"
  shell: bash
- name: Send Slack notification with custom result.
  if: always() && steps.network.outputs.OUTAGE == 'true'
  uses: ScribeMD/slack-templates@0.6.11
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
        uses: ScribeMD/slack-templates@0.6.11
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
        uses: ScribeMD/slack-templates@0.6.11
        with:
          bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
          channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
          template: assignee
```

### Send a custom notification

```yaml
- name: Send custom Slack notification.
  if: always()
  uses: ScribeMD/slack-templates@0.6.11
  with:
    bot-token: ${{ secrets.SLACK_TEMPLATES_BOT_TOKEN }}
    channel-id: ${{ secrets.SLACK_TEMPLATES_CHANNEL_ID }}
    message: "${{ github.actor }} requests approval to run workflow."
```

## Inputs

### Required

#### `bot-token`

The Slack API bot token for your custom app with `chat:write` scope.

#### `channel-id`

The ID of a Slack channel to send notifications to. Your bot should be a member.
Secondary-click on the channel in Slack, and select `Copy link` to copy a URL
containing the channel ID.

### Optional

#### `template`

default: `custom`

The type of Slack notification to send:

- `assignee`
- `custom` (requires `message`)
- `reviewers`
- `result`

#### `results` (`template: result` only)

default: `${{ job.status }}`

The job results to report via Slack. To report the result of an entire workflow,
use this action from a final notify job that depends on (a.k.a., `needs`) all
other jobs. Then, pass `join(needs.*.result, ' ')`. The highest ranking result
will be reported:

1. `failure`
1. `cancelled`
1. `success`
1. `skipped`

Alternatively, a custom result may be passed provided that it is quoted for use
as a Bash command line argument.

#### `message` (`template: custom` only)

default: `Pass message or template to slack-templates.`

A custom Slack message to send.

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

## Permissions

The `contents:read` and `pull-requests:read`
[permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)
are required in private repositories to determine the pull request associated
with a push event since the push event itself doesn't contain this information.

## Changelog

Please refer to [`CHANGELOG.md`](CHANGELOG.md).
