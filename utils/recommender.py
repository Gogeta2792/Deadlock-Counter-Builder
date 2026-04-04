"""Rank counter items by how many selected enemy heroes they cover."""

from __future__ import annotations

from typing import List

from utils.data_loader import GameData, counter_items_for_hero


def recommend_items(
    selected_heroes: List[str],
    game_data: GameData,
) -> List[dict]:
    """
    Count how many selected heroes each item counters.

    Returns rows sorted by coverage (high first), then item name (A–Z).
    Each row: ``item``, ``coverage_count``, ``countered_heroes`` (sorted names).
    """
    item_to_heroes: dict[str, set[str]] = {}

    for hero in selected_heroes:
        for item in set(counter_items_for_hero(game_data, hero)):
            item_to_heroes.setdefault(item, set()).add(hero)

    rows = [
        {
            "item": item,
            "coverage_count": len(heroes),
            "countered_heroes": sorted(heroes),
        }
        for item, heroes in item_to_heroes.items()
    ]

    rows.sort(key=lambda r: (-r["coverage_count"], r["item"].lower()))
    return rows
