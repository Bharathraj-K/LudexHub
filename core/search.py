from __future__ import annotations

from rapidfuzz import fuzz

from models.game import Game


def search_games(query: str, games: list[Game]) -> list[Game]:
    if not query.strip():
        return sorted(games, key=lambda g: (not g.favorite, g.name.lower()))

    scored: list[tuple[float, Game]] = []
    query_lower = query.lower()

    for game in games:
        name_lower = game.name.lower()
        score = fuzz.partial_ratio(query_lower, name_lower)

        if name_lower.startswith(query_lower):
            score += 20
        elif query_lower in name_lower:
            score += 10

        if game.favorite:
            score += 5

        scored.append((score, game))

    scored.sort(key=lambda x: (-x[0], x[1].name.lower()))
    return [game for score, game in scored if score >= 40]
