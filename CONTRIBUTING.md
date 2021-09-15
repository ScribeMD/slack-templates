# Contributing Guide

<!--TOC-->

- [Contributing Guide](#contributing-guide)
  - [Setup](#setup)
  - [Expectations](#expectations)
  - [Editors](#editors)

<!--TOC-->

## Setup

- [Install Docker](https://docs.docker.com/get-docker/).
- Install the version of Python specified as the `default_language_version` in
  [.pre-commit-config.yaml](.pre-commit-config.yaml) and
  the `[tool.poetry.dependencies]` section of [pyproject.toml](pyproject.toml).
- [Install Poetry](https://python-poetry.org/docs/) by running
  `pip install poetry>=1.2.0a2`.
- Change directories to the root of this repository.
- Run `poetry install` to install all Python dependencies.
- Run `poetry shell` to activate the Poetry virtual environment.
- Run `pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push`
  to install all pre-commit hooks.

## Expectations

- New templates are generally very welcome.
- For non-trivial issues, you may save yourself time by filing an issue first
  so we can discuss how best to address your proposal.
- Thoroughly review [README.md](README.md), and include any pertinent changes
  to the documentation in your change.
- The purpose of pre-commit hooks is to automate the trivial aspects of code
  review. Please address all issues found by pre-commit hooks that they don't
  fix automatically before opening a pull request. If you are stumped, please
  consult the documentation of the tool run by the failing hook. If you are
  still stumped, ask questions in an appropriate forum, such as
  [Stack Overflow](https://stackoverflow.com/), a tool-specific forum, or your
  work Slack if applicable.
- We use the Python-based
  [Commitizen](https://commitizen-tools.github.io/commitizen/), not to be
  confused with the Node.js-based
  [Commitizen](http://commitizen.github.io/cz-cli/). This helps to maintain a
  clear revision history. The
  [bump-version](.github/workflows/bump-version.yaml) job automatically bumps
  the project version in [pyproject.toml](pyproject.toml), appends to
  [CHANGELOG.md](CHANGELOG.md), and tags versions.
  You can either write
  [Conventional Commits](https://www.conventionalcommits.org/) by hand or run
  `cz commit` from within the Poetry virtual environment for guidance.

## Editors

[VSCode](https://code.visualstudio.com/) is recommended as this repository
configures it to run many of our linters as you edit.

- When prompted, install the extensions recommended by the workspace.
- When prompted, select the Python interpreter from the virtual environment
  Poetry created for this repository.
