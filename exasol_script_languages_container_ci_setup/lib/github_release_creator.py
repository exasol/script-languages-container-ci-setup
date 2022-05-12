import os

from github import Github


class GithubReleaseCreator(object):
    """
    Implements creation of a Github Draft Release.
    See https://docs.github.com/en/rest/releases/releases for details.
    The access token needs to be stored in the environment variable GITHUB_TOKEN.
    Returns the internal ID of the new release.
    """
    def __init__(self):
        self._token = os.getenv("GITHUB_TOKEN")

    def create_release(self, repo_name: str, branch: str, title: str) -> int:
        gh = Github(self._token)
        gh_repo = gh.get_repo(repo_name)
        release = gh_repo.create_git_release(tag="", name=title, message="Test-Release",
                                             draft=True, prerelease=True, target_commitish=branch)
        return release.id
