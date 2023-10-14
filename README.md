# pytest-gitconfig

[![CI](https://github.com/noirbizarre/pytest-gitconfig/actions/workflows/ci.yml/badge.svg)](https://github.com/noirbizarre/pytest-gitconfig/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/noirbizarre/pytest-gitconfig/main.svg)](https://results.pre-commit.ci/latest/github/noirbizarre/pytest-gitconfig/main)
[![PyPI](https://img.shields.io/pypi/v/pytest-gitconfig)](https://pypi.org/project/pytest-gitconfig/)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-gitconfig)](https://pypi.org/project/pytest-gitconfig/)
[![codecov](https://codecov.io/gh/noirbizarre/pytest-gitconfig/branch/main/graph/badge.svg?token=OR4JScC2Lx)](https://codecov.io/gh/noirbizarre/pytest-gitconfig)

Provide a gitconfig sandbox for testing

## Getting started

Install `pytest-gitconfig`:

```shell
# pip
pip install pytest-gitconfig
# pipenv
pipenv install pytest-gitconfig
# PDM
pdm add pytest-gitconfig
```

Then in your `conftest.py`:

```python
# All tests are using the sandboxed gitconfig
pytestmark = pytest.mark.usefixtures("gitconfig")
```

or if you want to customize or depend on it

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from pytest_gitconfig import GitConfig

@pytest.fixture
def git_user_name() -> str:
  return "John Doe"

@pytest.fixture
def fixture_depending_on_gitconfig(gitconfig: GitConfig) -> Whatever:
    # You can set values, the 4 following statements are equivalents
    gitconfig.set({"some": {key: value}}) # nested dicts form
    gitconfig.set(some={key: value})      # dicts as kwargs form
    gitconfig.set({"some.key": value})    # dict with dotted keys form
    gitconfig.set(**{"some.key": value})  # kwargs with dotted keys form
    # Or read them
    data = gitconfig.get("some.key")
    data = gitconfig.get("some.key", "fallback")
    # If you need the path to the gitconfig file
    GIT_CONFIG_GLOBAL = str(gitconfig)
    return whatever
```

Note that the `gitconfig` fixture being session-scoped (avoiding the performance hit of creating a gitconfig file for each test),
set values are persistent for the whole session and should be defined once preferably in your `conftest.py`.
But if you need to temporarily override some value, you can use the `override()` context manager which is accepting the same parameters as `set()`.

This allows to define a fixture with another scope or to override it directly during a test:

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
  from pytest_gitconfig import GitConfig

@pytest.fixture(scope="module")
def gitconfig(gitconfig: GitConfig) -> Iterator[GitConfig]:
    # Define a gitconfig values for the module
    with gitconfig.override({"some.key": value}):
        yield gitconfig


def test_something(gitconfig):
    with gitconfig.override({"other.key": value}):
        # Do something depending on those overridden values
```

## Provided fixtures

All fixtures are session-scoped.

### `gitconfig -> pytest_gitconfig.GitConfig`

This is the main fixture which is creating a new and clean git config file for the test session.

By default, it will set 3 settings:

- `user.name`
- `user.email`
- `init.defaultBranch`

The fixture when required provide a `pytest_gitconfig.GitConfig` object with the following methods:

- `gitconfig.set()` accepting either a `dict` or kwargs, as parsed data sections as dict or dotted-key-values.
- `gitconfig.get()` to get a setting given its dotted key. Get a 2nd default value. Raise `KeyError` if config does not exists and `default` is not provided
- `gitconfig.override()` a context manager setting the values and restoring them on exit

It works by monkeypatching the `GIT_CONFIG_GLOBAL` environment variable.
So, if you rely on this in a context where `os.environ` is ignored, you should patch it yourself using this fixture.

### `git_user_name -> str`

Provide the initial `user.name` setting. By default `pytest_gitconfig.DEFAULT_GIT_USER_NAME`.
Override to provide a different initial value.

### `git_user_email -> str`

Provide the initial `user.email` setting. By default `pytest_gitconfig.DEFAULT_GIT_USER_EMAIL`.
Override to provide a different initial value.

### `git_init_default_branch -> str`

Provide the initial `init.defaultBranch` setting. By default `pytest_gitconfig.DEFAULT_GIT_BRANCH` (`main`).
Override to provide a different initial value.

### `sessionpatch -> pytest.MonkeyPatch`

A `pytest.MonkeyPatch` session instance.
