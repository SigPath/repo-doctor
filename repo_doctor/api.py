"""Pobieranie repozytoriów użytkownika z GitHub API (fetch wstrzykiwalny → testy bez sieci)."""
import json
import os
import urllib.request
from typing import Callable, List


def http_get_json(url: str) -> List[dict]:
    headers = {"User-Agent": "repo-doctor/1.0", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def fetch_repos(user: str, fetch: Callable[[str], List[dict]] = http_get_json) -> List[dict]:
    """Lista publicznych repo użytkownika (bez forków na poziomie wywołania API)."""
    url = f"https://api.github.com/users/{user}/repos?per_page=100&sort=pushed&type=owner"
    repos = fetch(url)
    return [r for r in repos if not r.get("fork")]
