"""Streamlit UI for Deadlock counter item recommendations (heroes + item icons)."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from utils.data_loader import (
    DataValidationError,
    counter_items_for_hero,
    hero_icon_path,
    item_icon_path,
    load_game_data,
    resolve_asset_path,
    sorted_hero_names,
)
from utils.recommender import recommend_items

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "character_counters.json"
MAX_SELECTIONS = 6

HERO_ICON_WIDTH = 56
ITEM_ICON_WIDTH = 52


@st.cache_data
def get_game_data_cached(path_str: str) -> dict:
    return load_game_data(path_str)


def reset_selection() -> None:
    st.session_state["enemy_selection"] = []


def render_image_or_fallback(
    *,
    rel_path: str,
    fallback_text: str,
    width: int,
) -> None:
    """Show a local image if it exists under the project root; otherwise a compact text badge."""
    resolved = resolve_asset_path(PROJECT_ROOT, rel_path)
    if resolved is not None:
        st.image(str(resolved), width=width)
        return

    initials = "".join(part[0] for part in fallback_text.split()[:2] if part).upper() or "?"
    safe_title = html.escape(fallback_text, quote=True)
    st.markdown(
        f'<div title="{safe_title}" style="width:{width}px;min-height:{width}px;'
        f"max-height:{width}px;display:flex;align-items:center;justify-content:center;"
        "background:linear-gradient(145deg,#2d3748,#1a202c);color:#e2e8f0;"
        f"border-radius:10px;font-weight:700;font-size:{max(11, width // 5)}px;"
        'border:1px solid #4a5568;">'
        f"{initials}</div>",
        unsafe_allow_html=True,
    )


def render_hero_row(hero_name: str, game_data: dict) -> None:
    rel = hero_icon_path(game_data, hero_name)
    c_img, c_name = st.columns([0.22, 0.78], gap="small")
    with c_img:
        render_image_or_fallback(
            rel_path=rel,
            fallback_text=hero_name,
            width=HERO_ICON_WIDTH,
        )
    with c_name:
        st.markdown(f"**{hero_name}**")


def render_selected_heroes_panel(selected: list[str], game_data: dict) -> None:
    st.markdown("##### Selected enemies")
    if not selected:
        st.caption("Pick up to 6 heroes from the list above.")
        return

    for row_start in range(0, len(selected), 3):
        chunk = selected[row_start : row_start + 3]
        cols = st.columns(len(chunk), gap="small")
        for col, hero_name in zip(cols, chunk):
            with col:
                render_hero_row(hero_name, game_data)


def render_countered_heroes_chips(game_data: dict, hero_names: list[str]) -> None:
    """Small icon + name for each hero this item counters."""
    if not hero_names:
        st.caption("None of the selected heroes.")
        return
    cols = st.columns(len(hero_names), gap="small")
    for col, hero_name in zip(cols, hero_names):
        with col:
            render_image_or_fallback(
                rel_path=hero_icon_path(game_data, hero_name),
                fallback_text=hero_name,
                width=40,
            )
            st.caption(hero_name)


def render_recommendations(selected: list[str], game_data: dict) -> None:
    n = len(selected)
    rows = recommend_items(selected, game_data)

    st.subheader("Recommended counter items")
    st.caption("Sorted by how many of your selected enemies each item counters.")

    if not rows:
        st.info("No counter items were found for the current selection.")
        return

    for row in rows:
        coverage = row["coverage_count"]
        item_name = row["item"]
        countered = row["countered_heroes"]
        ratio = coverage / n if n else 0.0

        if coverage >= max(1, n - 1):
            strength = "Strong coverage"
        elif coverage >= max(1, n // 2):
            strength = "Solid pick"
        else:
            strength = "Situational"

        item_rel = item_icon_path(game_data, item_name)

        with st.container(border=True):
            head = st.columns([0.12, 0.58, 0.30], gap="medium")
            with head[0]:
                render_image_or_fallback(
                    rel_path=item_rel,
                    fallback_text=item_name,
                    width=ITEM_ICON_WIDTH,
                )
            with head[1]:
                st.markdown(f"### {item_name}")
                st.markdown(
                    f"**Counters {coverage}/{n} selected heroes** — _{strength}_"
                )
                st.progress(ratio, text=f"{int(ratio * 100)}% of selected roster")
            with head[2]:
                st.metric(
                    "Coverage",
                    f"{coverage} / {n}",
                    help="How many of your selected enemies this item counters.",
                )

            st.markdown("**Covered heroes**")
            render_countered_heroes_chips(game_data, countered)


def render_per_hero_breakdown(selected: list[str], game_data: dict) -> None:
    with st.expander("Per-hero counter lists", expanded=False):
        for hero_name in selected:
            items = counter_items_for_hero(game_data, hero_name)
            sub = st.columns([0.14, 0.86], gap="small")
            with sub[0]:
                render_image_or_fallback(
                    rel_path=hero_icon_path(game_data, hero_name),
                    fallback_text=hero_name,
                    width=HERO_ICON_WIDTH,
                )
            with sub[1]:
                st.markdown(f"**{hero_name}**")
                if items:
                    for it in items:
                        ir, tr = st.columns([0.08, 0.92], gap="small")
                        with ir:
                            render_image_or_fallback(
                                rel_path=item_icon_path(game_data, it),
                                fallback_text=it,
                                width=36,
                            )
                        with tr:
                            st.markdown(it)
                else:
                    st.caption("No items listed for this hero.")


def main() -> None:
    st.set_page_config(page_title="Deadlock Counter Builder", page_icon="🎯", layout="wide")

    st.title("Deadlock Counter Builder")
    st.write(
        "Select **6** enemy heroes. Recommendations rank items by how many of those six "
        "each item counters."
    )

    try:
        game_data = get_game_data_cached(str(DATA_PATH))
    except FileNotFoundError as err:
        st.error(str(err))
        st.stop()
    except DataValidationError as err:
        st.error(f"Data validation error: {err}")
        st.stop()
    except Exception as err:  # noqa: BLE001
        st.error(f"Unexpected error while loading data: {err}")
        st.stop()

    all_heroes = sorted_hero_names(game_data)

    left, right = st.columns([1, 1.35], gap="large")

    with left:
        st.subheader("Enemy roster")
        st.caption("Search by name. Streamlit’s multiselect cannot show images; icons appear below.")

        selected = st.multiselect(
            "Choose enemy heroes",
            options=all_heroes,
            default=st.session_state.get("enemy_selection", []),
            max_selections=MAX_SELECTIONS,
            key="enemy_selection",
            placeholder="Type to filter heroes…",
            help=f"Select exactly {MAX_SELECTIONS} heroes to unlock ranked items.",
        )

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Selected", f"{len(selected)} / {MAX_SELECTIONS}")
        with m2:
            st.button("Clear selection", on_click=reset_selection, type="secondary")

        render_selected_heroes_panel(selected, game_data)

        if len(selected) < MAX_SELECTIONS:
            st.info(f"Choose **{MAX_SELECTIONS - len(selected)}** more hero(es) to see recommendations.")
        elif len(selected) == MAX_SELECTIONS:
            render_per_hero_breakdown(selected, game_data)

    with right:
        if len(selected) == MAX_SELECTIONS:
            render_recommendations(selected, game_data)
        else:
            st.subheader("Recommended counter items")
            st.info(
                f"Recommendations unlock when **{MAX_SELECTIONS}** enemies are selected. "
                "Use the panel on the left to finish your pick."
            )


if __name__ == "__main__":
    main()
