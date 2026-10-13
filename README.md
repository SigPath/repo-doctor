# Repo Doctor

**Audyt własnych repozytoriów GitHub**: punkty za opis, licencję, tematy, demo,
świeżość i zawartość — z konkretnymi zaleceniami i ocenami A–D. Raport HTML publikowany
automatycznie, na **prawdziwych danych** z GitHub API.

→ **Raport na żywo:** https://sigpath.github.io/repo-doctor/ (audyt konta SigPath, odświeżany przy każdym pushu)

## Kryteria (100 pkt)

| Kryterium | Punkty | Jak spełnić |
|---|---|---|
| Opis | 15 | ustaw opis repo |
| Licencja | 20 | dodaj LICENSE (MIT/…) |
| Tematy | 15 | ≥1 topic w ustawieniach |
| Demo | 15 | ustaw homepage (GitHub Pages!) |
| Świeżość | 20 | push < 30 dni (12 pkt do 90 dni) |
| Rozmiar | 15 | ≥ 5 KB zawartości |

Oceny: **A** ≥ 85 · **B** ≥ 70 · **C** ≥ 50 · **D** < 50. Forki pomijane.

## Szybki start

```bash
python3 tests/test_doctor.py                     # 6 testów, fixture'y bez sieci
python3 -m repo_doctor audit --user SigPath      # audyt → docs/index.html + konsola
# opcjonalnie wyższy limit API: export GITHUB_TOKEN=...
```

## Uczciwe ograniczenia

- v1 korzysta tylko z metadanych listy repo (opis/licencja/topics/homepage/pushed_at/size);
  w planach: obecność testów i CI (dodatkowe zapytania per repo),
- oceny to samoocena Warsztatu — Repo Doctor mówi „co ulepszyć", nie „czy kod jest dobry".

## Licencja

MIT
