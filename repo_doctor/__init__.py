"""Repo Doctor — audyt własnych repozytoriów GitHub: co wygląda dobrze, co poprawić."""
from .checks import audit_repo, grade
from .api import fetch_repos
from .report import render_html, render_console

__version__ = "1.0.0"
__all__ = ["audit_repo", "grade", "fetch_repos", "render_html", "render_console", "__version__"]
