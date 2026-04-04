"""Load and validate counter data (heroes, items, local icon paths)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict


class DataValidationError(ValueError):
    """Raised when game data JSON is missing required keys or has wrong types."""


class HeroEntry(TypedDict, total=False):
    icon: str
    counter_items: list[str]


class ItemEntry(TypedDict, total=False):
    icon: str


class GameData(TypedDict):
    heroes: dict[str, HeroEntry]
    items: dict[str, ItemEntry]


def load_game_data(file_path: str | Path) -> GameData:
    """Load JSON with top-level ``heroes`` and ``items`` objects."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        raw: Any = json.load(handle)

    return validate_game_data(raw)


def validate_game_data(data: object) -> GameData:
    """Validate ``{ "heroes": {...}, "items": {...} }`` shape."""
    if not isinstance(data, dict):
        raise DataValidationError("Top-level JSON value must be an object.")

    heroes_raw = data.get("heroes")
    items_raw = data.get("items")

    if not isinstance(heroes_raw, dict):
        raise DataValidationError('Missing or invalid "heroes" object.')
    if not isinstance(items_raw, dict):
        raise DataValidationError('Missing or invalid "items" object.')

    heroes: dict[str, HeroEntry] = {}
    for name, entry in heroes_raw.items():
        if not isinstance(name, str):
            raise DataValidationError("All hero names must be strings.")
        if not isinstance(entry, dict):
            raise DataValidationError(f'Hero "{name}" must be an object with icon / counter_items.')
        icon = entry.get("icon", "")
        if icon is not None and not isinstance(icon, str):
            raise DataValidationError(f'Hero "{name}" icon must be a string path or omitted.')
        raw_items = entry.get("counter_items", [])
        if not isinstance(raw_items, list):
            raise DataValidationError(f'Hero "{name}" counter_items must be a list.')
        if not all(isinstance(x, str) for x in raw_items):
            raise DataValidationError(f'Hero "{name}" counter_items must be strings only.')
        deduped = sorted({x for x in raw_items})
        heroes[name] = {
            "icon": icon or "",
            "counter_items": deduped,
        }

    items: dict[str, ItemEntry] = {}
    for name, entry in items_raw.items():
        if not isinstance(name, str):
            raise DataValidationError("All item names must be strings.")
        if not isinstance(entry, dict):
            raise DataValidationError(f'Item "{name}" must be an object with an optional icon path.')
        icon = entry.get("icon", "")
        if icon is not None and not isinstance(icon, str):
            raise DataValidationError(f'Item "{name}" icon must be a string path or omitted.')
        items[name] = {"icon": icon or ""}

    return {"heroes": heroes, "items": items}


def resolve_asset_path(project_root: Path, relative_path: str | None) -> Path | None:
    """
    Resolve a project-relative asset path to an absolute path only if the file exists
    and stays inside ``project_root`` (avoids ``..`` escape).
    """
    if not relative_path or not str(relative_path).strip():
        return None

    root = project_root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None

    return candidate if candidate.is_file() else None


def hero_icon_path(game_data: GameData, hero_name: str) -> str:
    entry = game_data["heroes"].get(hero_name)
    if not entry:
        return ""
    return str(entry.get("icon") or "")


def item_icon_path(game_data: GameData, item_name: str) -> str:
    entry = game_data["items"].get(item_name)
    if not entry:
        return ""
    return str(entry.get("icon") or "")


def counter_items_for_hero(game_data: GameData, hero_name: str) -> list[str]:
    entry = game_data["heroes"].get(hero_name)
    if not entry:
        return []
    return list(entry.get("counter_items") or [])


def sorted_hero_names(game_data: GameData) -> list[str]:
    return sorted(game_data["heroes"].keys())
