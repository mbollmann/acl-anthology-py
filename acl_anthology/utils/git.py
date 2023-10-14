# Copyright 2023 Marcel Bollmann <marcel@bollmann.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from git import Repo
from os import PathLike
from pathlib import Path

from .logging import get_logger


log = get_logger()


def clone_or_pull_from_repo(repo_url: str, local_path: PathLike[str]) -> None:
    """Clones a Git repository, or pulls from remote if it already exists.

    Arguments:
        repo_url: The URL of a Git repo.
        local_path: The local path containing the repo.  If it doesn't exist, we will attempt to clone the repo into it; if it exists, we assume it already contains the repo and will attempt to pull from 'origin'.
    """
    path = Path(local_path)
    log.debug(f"Using local repository folder: {path}")
    if path.exists():
        repo = Repo(path)
        if repo.remote().url != repo_url:
            log.error(
                (
                    "Repository folder exists, but doesn't match the given URL:\n",
                    f"   {repo.remote().url} != {repo_url}",
                )
            )
        log.info(f"Fetching updates from: {repo_url}")
        repo.remote().pull(force=True)
    else:
        log.info(f"Cloning repository: {repo_url}")
        repo = Repo.clone_from(repo_url, path, single_branch=True, depth=1)
