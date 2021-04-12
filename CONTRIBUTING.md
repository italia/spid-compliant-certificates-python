# Contributing guidelines

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to Python version of
**spid-compliant-certificates** project.
These are mostly guidelines, not rules. Use your best judgment, and feel free
to propose changes to this document in a pull request.

## How to contribute

1.  If you found something to add/fix, open an issue an discuss with the community

2.  Once ready, fork the repository (or pull from `main` if already forked)

3.  In your fork, create a branch starting from `main` and name it by following the
    [naming conventions](#branches-naming-conventions)

4.  Make your changes by following the [coding guidelines](#coding-guidelines)

5.  Push the changes on your branch and create a pull request

6.  Wait for a review

## Coding guidelines

1.  Use four spaces for intentation (leave TABS to Java lovers)

2.  Use type hints (see [PEP484](https://www.python.org/dev/peps/pep-0484/))
    when a new function is defined

3.  Use `\n` as end of line (we mainly develop on Linux)

4.  Before pushing your Python code, lint it with
    [`flake8`](https://flake8.pycqa.org/en/latest/)
    and [`isort`](https://pycqa.github.io/isort/)
    (see [PEP8](https://www.python.org/dev/peps/pep-0008/))

5.  Before pushing your changes on Dockerfiles, lint them with
    [`hadolint`](https://github.com/hadolint/hadolint)

## Branches naming conventions

Releases are issued by making use of
[Release Drafter](https://github.com/release-drafter/release-drafter) action.
In order to propery work, some naming conventions for branches must be followed.

### Bugfix

If you're working on a bugfix, please name your local branch with one of
the following prefixes:

-   `bug` (e.g. `bug/wrong-url-in-configuration`)
-   `bugfix` (e.g. `bugfix/wrong-url-in-configuration`)
-   `fix` (e.g. `fix/wrong-url-in-configuration`)

### New feature

If you're working on a new feature, please name your local branch with one
of the following prefixes:

-   `enhancement` (e.g. `enhancement/enable-2fa-with-solokey`)
-   `feat` (e.g. `feat/enable-2fa-with-solokey`)
-   `feature` (e.g. `feature/enable-2fa-with-solokey`)

### Maintenance

If you're working on maintenance tasks (e.g. documentation, repository management, source styling), please name your local branch with one of the following prefixes:

-   `chore` (e.g. `chore/remove-trailing-whitespaces`)
-   `style` (e.g. `style/remove-trailing-whitespaces`)
