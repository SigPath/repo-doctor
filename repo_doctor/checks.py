"""Kryteria audytu i punktacja. Wejście: słownik jak w GitHub API /repos/{user}/repos."""
from datetime import datetime, timezone
from typing import Dict, List, Tuple

CHECK_WEIGHTS = {
    "opis": 15,
    "licencja": 20,
    "tematy": 15,
    "demo": 15,
    "swiezosc": 20,
    "rozmiar": 15,
}


def _days_since(iso: str) -> float:
    if not iso:
        return 9999.0
    pushed = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - pushed).total_seconds() / 86400


def audit_repo(repo: Dict) -> Dict:
    """Zwraca {repo, url, score, grade, hits, misses, is_fork}."""
    license_info = repo.get("license") or {}
    spdx = license_info.get("spdx_id")
    days = _days_since(repo.get("pushed_at", ""))

    hits: List[str] = []
    misses: List[Tuple[str, int, str]] = []
    score = 0

    def add(name: str, passed: bool, tip: str = "") -> None:
        nonlocal score
        points = CHECK_WEIGHTS[name]
        if passed:
            score += points
            hits.append(name)
        else:
            misses.append((name, points, tip))

    add("opis", bool((repo.get("description") or "").strip()),
        "Dodaj opis: jedno zdanie, co to robi i dla kogo.")
    add("licencja", bool(spdx and spdx not in ("NOASSERTION", "Other")),
        "Dodaj plik LICENSE (MIT to dobry start dla portfolio).")
    add("tematy", len(repo.get("topics") or []) > 0,
        "Dodaj tematy (topics) — znajdują Cię w wyszukiwarce GitHuba.")
    add("demo", bool((repo.get("homepage") or "").strip()),
        "Ustaw homepage — żywe demo liczy się podwójnie.")
    if days < 30:
        add("swiezosc", True)
    elif days < 90:
        score += 12  # częściowe punkty za świeżość
        misses.append(("swiezosc", 8, f"Ostatni push {days:.0f} dni temu — odśwież projekt."))
    else:
        add("swiezosc", False, f"Ostatni push {days:.0f} dni temu — odśwież albo oznacz jako ukończony.")
    add("rozmiar", repo.get("size", 0) >= 5,
        "Repo wygląda na puste — dodaj kod albo README.")

    score = max(0, min(100, score))
    return {
        "repo": repo.get("name", "?"),
        "url": repo.get("html_url", "#"),
        "score": score,
        "grade": grade(score),
        "hits": hits,
        "misses": misses,
        "is_fork": bool(repo.get("fork")),
    }


def grade(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"
