"""Search helpers: match book title, author, and city together."""

from __future__ import annotations

from typing import Any


def entry_city(entry: dict[str, Any]) -> str:
    city = entry.get("city")
    if city is not None and str(city).strip():
        return str(city).strip()
    loc = str(entry.get("location_name", "")).strip()
    if "," in loc:
        return loc.split(",")[-1].strip()
    return loc


def entry_matches_query(entry: dict[str, Any], q: str) -> bool:
    if not q:
        return True
    title = str(entry.get("title", "")).lower()
    author = str(entry.get("author", "")).lower()
    city = entry_city(entry).lower()
    return q in title or q in author or q in city


def _suggest_score(entry: dict[str, Any], q: str) -> int:
    title = str(entry.get("title", "")).lower()
    author = str(entry.get("author", "")).lower()
    city = entry_city(entry).lower()
    score = 0
    if title.startswith(q):
        score += 120
    elif q in title:
        score += 85
    if author.startswith(q):
        score += 70
    elif q in author:
        score += 45
    if city.startswith(q):
        score += 55
    elif q in city:
        score += 35
    return score


def filter_entries_for_suggest(entries: list[dict[str, Any]], query: str, limit: int = 12) -> list[dict[str, Any]]:
    q = query.strip().lower()
    if not q:
        return []
    ranked: list[tuple[int, dict[str, Any]]] = []
    for e in entries:
        if not entry_matches_query(e, q):
            continue
        ranked.append((_suggest_score(e, q), e))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [e for _, e in ranked[:limit]]
