"""CLI Repo Doctor:  python3 -m repo_doctor audit --user SigPath --out docs/index.html"""
import argparse
import os
import sys
from typing import List

from .api import fetch_repos
from .checks import audit_repo
from .report import render_console, render_html


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(prog="repo_doctor", description="Audyt repozytoriów GitHub: punkty, oceny, konkretne zalecenia.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    audit_p = sub.add_parser("audit", help="przeaudytuj repozytoria użytkownika")
    audit_p.add_argument("--user", required=True)
    audit_p.add_argument("--out", default="docs/index.html", help="ścieżka raportu HTML")
    args = parser.parse_args(argv)
    if args.cmd != "audit":  # pragma: no cover
        parser.error("nieznana komenda")

    try:
        repos = fetch_repos(args.user)
    except Exception as e:
        print(f"BŁĄD pobierania repozytoriów: {e}", file=sys.stderr)
        return 2
    if not repos:
        print("BŁĄD: brak repozytoriów do audytu.", file=sys.stderr)
        return 2

    results = [audit_repo(r) for r in repos]
    results.sort(key=lambda r: r["score"], reverse=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(render_html(results, args.user))

    print(render_console(results))
    mean = round(sum(r["score"] for r in results) / len(results))
    print(f"\nRaport: {args.out} · średnia {mean}/100")
    return 0


if __name__ == "__main__":
    sys.exit(main())
