import pytest
import asyncio
from potpie.app.modules.code_provider.github.github_service import GithubService
from unittest.mock import AsyncMock, MagicMock, patch

# Using ChatGPT's help

@pytest.fixture
def mock_db_session(cd):

    mock_db = MagicMock()

    mock_db.query().filter().group_by().subquery.return_value.c.repo_name = "user/repo1"
    mock_db.query().filter().group_by().subquery.return_value.c.min_id = 1


    mock_project = MagicMock()
    mock_project.id = 1
    mock_project.repo_name = "user/repo1"
    mock_project.user_id = "1234"

    mock_db.query.join().all.return_value = [mock_project]
    return mock_db

@pytest.fixture
def mock_github_repo():

    mock_repo = MagicMock()
    mock_repo.default_branch = "main"
    mock_repo.get_branches.return_value = [MagicMock(name="main"), MagicMock(name="dev")]
    return mock_repo

@pytest.mark.asyncio
async def test_get_combined_user_repos(mock_db_session):

    instance = GithubService()
    instance.db = mock_db_session

    instance.get_repos_for_user = AsyncMock(return_value={"repositories": [{"full_name": "user/repo2"}]})

    result = await instance.get_combined_user_repos(user_id="1234")

    assert "repositories" in result
    assert len(result["repositories"]) == 2
    assert result["repositories"][0]["full_name"] == "user/repo2"
    assert result["repositories"][1]["full_name"] == "user/repo1"

@pytest.mark.asyncio
async def test_get_branch_list(mock_github_repo):

    instance = GithubService()

    instance.get_repo = MagicMock(return_value=(None, mock_github_repo))

    result = await instance.get_branch_list("user/repo1")

    assert "branches" in result
    assert result["branches"] == ["main", "dev"]


