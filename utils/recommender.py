"""Recommendation logic for Deadlock counter items."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

CharacterCounters = Dict[str, List[str]]


class DataValidationError(ValueError):
    """Raised when character counter data is malformed."""


def load_character_counters(file_path: str | Path) -> CharacterCounters:
    """Load and validate character counter data from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return validate_character_counters(data)


def validate_character_counters(data: object) -> CharacterCounters:
    """Validate data format: {character: [counter_item, ...]}"""
    if not isinstance(data, dict):
        raise DataValidationError("Top-level JSON value must be an object (dictionary).")

    validated: CharacterCounters = {}

    for character, items in data.items():
        if not isinstance(character, str):
            raise DataValidationError("All character names must be strings.")
        if not isinstance(items, list):
            raise DataValidationError(
                f"Counter items for '{character}' must be a list of strings."
            )
        if not all(isinstance(item, str) for item in items):
            raise DataValidationError(
                f"Counter items for '{character}' must only contain strings."
            )

        # De-duplicate per character to avoid counting the same item twice for one character.
        deduped_items = sorted(set(items))
        validated[character] = deduped_items

    return validated


def recommend_items(
    selected_characters: List[str],
    character_counters: CharacterCounters,
) -> List[dict]:
    """Build ranked recommendations based on item frequency across selected characters."""
    item_to_characters: Dict[str, set[str]] = {}

    for character in selected_characters:
        items = character_counters.get(character, [])
        for item in set(items):
            item_to_characters.setdefault(item, set()).add(character)

    recommendations = [
        {
            "item": item,
            "coverage_count": len(countered_characters),
            "countered_characters": sorted(countered_characters),
        }
        for item, countered_characters in item_to_characters.items()
    ]

    recommendations.sort(key=lambda row: (-row["coverage_count"], row["item"].lower()))
    return recommendations
