from __future__ import annotations

import os

import pytest

from pytest_gitconfig import GitConfig

USER_NAME = "Overridden user Name"
USER_EMAIL = "hello@nowhere.com"
DEFAULT_BRANCH = "master"

pytestmark = pytest.mark.mypy_testing


@pytest.fixture(scope="session")
def git_env_var(sessionpatch: pytest.MonkeyPatch):
    sessionpatch.setenv("GIT_WHATEVER", "whatever")


@pytest.fixture(scope="session")
def git_user_name() -> str:
    return USER_NAME


@pytest.fixture(scope="session")
def git_user_email() -> str:
    return USER_EMAIL


@pytest.fixture(scope="session")
def git_init_default_branch() -> str:
    return DEFAULT_BRANCH


def test_gitconfig_fixture_override(gitconfig: GitConfig):
    assert gitconfig.get("user.name") == USER_NAME
    assert gitconfig.get("user.email") == USER_EMAIL
    assert gitconfig.get("init.defaultBranch") == DEFAULT_BRANCH
    assert "GIT_WHATEVER" not in os.environ
