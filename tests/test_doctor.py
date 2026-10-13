"""Testy Repo Doctor — punktacja na sztucznych repo, bez sieci."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repo_doctor.api import fetch_repos  # noqa: E402
from repo_doctor.checks import audit_repo, grade  # noqa: E402
from repo_doctor.report import render_html, render_console  # noqa: E402


def perfect_repo():
    return {
        "name": "idealne", "html_url": "https://github.com/u/idealne",
        "description": "Coś robi.", "license": {"spdx_id": "MIT"},
        "topics": ["python"], "homepage": "https://demo.example",
        "pushed_at": "2026-10-13T10:00:00Z", "size": 500, "fork": False,
    }


def empty_repo():
    return {
        "name": "puste", "html_url": "https://github.com/u/puste",
        "description": None, "license": None, "topics": [],
        "homepage": None, "pushed_at": "2024-01-01T00:00:00Z", "size": 0, "fork": True,
    }


class TestScoring(unittest.TestCase):
    def test_perfect_repo_100(self):
        r = audit_repo(perfect_repo())
        self.assertEqual(r["score"], 100)
        self.assertEqual(r["grade"], "A")
        self.assertEqual(r["misses"], [])

    def test_empty_repo_niska_ocena(self):
        r = audit_repo(empty_repo())
        self.assertEqual(r["score"], 0)
        self.assertEqual(r["grade"], "D")
        self.assertTrue(r["is_fork"])
        self.assertEqual(len(r["misses"]), 6)

    def test_czesciowa_swiezosc_daje_12(self):
        repo = perfect_repo()
        repo["name"] = "stare"
        repo["pushed_at"] = "2026-08-01T10:00:00Z"  # ~73 dni przed 2026-10-13
        r = audit_repo(repo)
        self.assertEqual(r["score"], 92)
        self.assertEqual(r["misses"][0][1], 8)

    def test_oceny_graniczne(self):
        self.assertEqual(grade(100), "A")
        self.assertEqual(grade(85), "A")
        self.assertEqual(grade(84), "B")
        self.assertEqual(grade(70), "B")
        self.assertEqual(grade(50), "C")
        self.assertEqual(grade(49), "D")


class TestApi(unittest.TestCase):
    def test_fetch_filtrowanie_forkow(self):
        fake = [perfect_repo(), empty_repo()]
        repos = fetch_repos("ktoś", fetch=lambda url: fake)
        self.assertEqual(len(repos), 1)  # fork odfiltrowany
        self.assertEqual(repos[0]["name"], "idealne")


class TestReport(unittest.TestCase):
    def test_html_i_konsola(self):
        results = [audit_repo(perfect_repo()), audit_repo(empty_repo())]
        html = render_html(results, "testuser")
        self.assertIn("REPO·DOCTOR", html)
        self.assertIn("idealne", html)
        self.assertIn("puste", html)
        console = render_console(results)
        self.assertIn("[A]", console)
        self.assertIn("[D]", console)


if __name__ == "__main__":
    unittest.main()
