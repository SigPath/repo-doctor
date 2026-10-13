"""Raporty: HTML (do Pages) + konsola."""
import html
from datetime import datetime, timezone
from typing import List

_COLORS = {"A": "#3ecf8e", "B": "#ffb000", "C": "#e8890c", "D": "#ff6b6b"}


def render_html(results: List[dict], user: str) -> str:
    rows = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        color = _COLORS.get(r["grade"], "#9aa4b0")
        misses = "".join(
            f"<li><b>{html.escape(name)}</b> (+{points}) — {html.escape(tip)}</li>"
            for name, points, tip in r["misses"]
        )
        fork_note = " <span class='tag'>fork</span>" if r["is_fork"] else ""
        rows.append(f"""
<details{' open' if r['misses'] else ''}>
  <summary><span class="grade" style="background:{color}">{r['grade']}</span>
  <a href="{html.escape(r['url'])}">{html.escape(r['repo'])}</a>{fork_note}
  <span class="score">{r['score']}/100</span></summary>
  <ul>{misses if misses else '<li>Wszystkie kryteria spełnione ✅</li>'}</ul>
</details>""")

    mean = round(sum(r["score"] for r in results) / len(results)) if results else 0
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Repo Doctor — audyt @{html.escape(user)}</title>
<style>
:root {{ color-scheme: dark; }}
body {{ background:#101418; color:#e8ebef; font-family: system-ui, sans-serif; margin:0; padding:40px 20px; }}
main {{ max-width: 820px; margin:0 auto; }}
h1 {{ font-size:26px; }} h1 span {{ color:#ffb000; }}
.meta {{ color:#9aa4b0; font-size:13px; font-family:ui-monospace,monospace; margin:6px 0 26px; }}
details {{ border:1px solid #2a333e; margin-bottom:10px; padding:12px 16px; background:#171d24; }}
summary {{ cursor:pointer; display:flex; align-items:center; gap:12px; }}
.grade {{ color:#101418; font-weight:800; padding:2px 10px; border-radius:4px; font-family:ui-monospace,monospace; }}
summary a {{ color:#e8ebef; text-decoration:none; font-weight:600; }}
summary a:hover {{ color:#ffb000; }}
.score {{ margin-left:auto; font-family:ui-monospace,monospace; color:#9aa4b0; }}
ul {{ margin:12px 0 0; padding-left:20px; color:#9aa4b0; font-size:13.5px; }}
li {{ margin-bottom:4px; }}
.tag {{ border:1px solid #2a333e; color:#9aa4b0; font-size:10px; padding:1px 6px; }}
.foot {{ color:#9aa4b0; font-size:12px; margin-top:30px; }}
.foot a {{ color:#ffb000; }}
</style></head>
<body><main>
<h1><span>REPO·DOCTOR</span> — audyt @{html.escape(user)}</h1>
<p class="meta">wygenerowano {stamp} · {len(results)} repozytoriów · średnia {mean}/100</p>
{''.join(rows)}
<p class="foot">Audyt wykonany przez <a href="https://github.com/SigPath/repo-doctor">Repo Doctor</a> · Marcin Burda · <a href="https://burda.eu.org">burda.eu.org</a></p>
</main></body></html>"""


def render_console(results: List[dict]) -> str:
    lines = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        lines.append(f"  [{r['grade']}] {r['repo']:28s} {r['score']:3d}/100")
        for name, points, tip in r["misses"]:
            lines.append(f"        - {name} (+{points}): {tip}")
    return "\n".join(lines)
