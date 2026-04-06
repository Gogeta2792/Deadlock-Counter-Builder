"""Streamlit UI for Deadlock counter item recommendations (heroes + item icons)."""

from __future__ import annotations

import base64
import hashlib
import html
import mimetypes
from pathlib import Path
from typing import Collection

import streamlit as st

from utils.data_loader import (
    DataValidationError,
    build_categorized_item_icon_index,
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
MAX_PURCHASED_ITEMS = 12

HERO_ICON_WIDTH = 56
ITEM_ICON_WIDTH = 52
PURCHASED_ITEM_ICON_WIDTH = 48
SELECTED_ENEMY_ITEM_ICONS_PER_ROW = 10
PER_HERO_ITEM_ICON_WIDTH = 48
PURCHASED_ITEMS_ICONS_PER_ROW = 5

# Placeholder entries in JSON — not assignable to heroes; omit from "purchased" picker.
_ITEMS_EXCLUDED_FROM_PURCHASED: frozenset[str] = frozenset(
    {
        "(Example) New Item Alpha",
        "(Example) New Item Beta",
    }
)


@st.cache_data(show_spinner=False)
def _cached_asset_data_uri(path_and_mtime: tuple[str, float]) -> tuple[str, str]:
    """Return (mime, base64) for a local asset file; mtime in the key invalidates when the file changes."""
    path_str, _ = path_and_mtime
    p = Path(path_str)
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    mime, _ = mimetypes.guess_type(p.name)
    if not mime:
        mime = "image/png"
    return mime, b64


def inject_responsive_css() -> None:
    """Narrow-viewport tweaks via keyed containers (st-key-*) and Streamlit test ids."""
    st.markdown(
        """
<style>
@media (max-width: 900px) {
  .st-key-dcb_main_split > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  .st-key-dcb_main_split > [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }
  .st-key-dcb_main_split > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  .st-key-dcb_main_split > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: 100% !important;
    min-width: 0 !important;
    flex: 1 1 auto !important;
  }
}
/* Only the two-card row, not nested rows inside each card */
@media (max-width: 768px) {
  [class*="st-key-dcb_rec_pair_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  [class*="st-key-dcb_rec_pair_"] > [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }
  [class*="st-key-dcb_rec_pair_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [class*="st-key-dcb_rec_pair_"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: 100% !important;
    min-width: 0 !important;
  }
}
@media (max-width: 640px) {
  [class*="st-key-dcb_rh_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  [class*="st-key-dcb_rh_"] > [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }
  [class*="st-key-dcb_rh_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [class*="st-key-dcb_rh_"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: 100% !important;
    min-width: 0 !important;
  }
  [class*="st-key-dcb_hero_row_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  [class*="st-key-dcb_hero_row_"] > [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }
  [class*="st-key-dcb_hero_row_"] > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [class*="st-key-dcb_hero_row_"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: 100% !important;
    min-width: 0 !important;
  }
}
@media (max-width: 520px) {
  .st-key-dcb_enemy_pick_row > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  .st-key-dcb_enemy_pick_row > [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    align-items: stretch !important;
  }
  .st-key-dcb_enemy_pick_row > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  .st-key-dcb_enemy_pick_row > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    width: 100% !important;
    min-width: 0 !important;
  }
}
.stApp [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
  min-width: min(100%, 3.25rem) !important;
}
/* Selected Enemies: counter items are icon-only; columns only need to fit the tile. */
[class*="st-key-dcb_hero_items_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
  min-width: min(100%, 3rem) !important;
}
.stApp img {
  max-width: 100%;
  height: auto;
}
/* Icon-grid labels: shrink to fit column width; wrap only at spaces (no mid-word breaks). */
.dcb-label-fit {
  width: 100%;
  box-sizing: border-box;
  text-align: center;
  margin: 0.15rem 0 0 0;
  line-height: 1.25;
  word-break: normal !important;
  overflow-wrap: normal !important;
  hyphens: none;
  color: var(--st-gray-text-color, var(--st-text-color, #31333F));
  font-size: 0.75rem;
}
@supports (font-size: 1cqi) {
  .dcb-label-fit {
    container-type: inline-size;
    font-size: max(0.55rem, min(0.8125rem, calc(100cqi / (var(--label-chars, 8) * 0.52))));
  }
}
.dcb-label-fit.dcb-owned-line {
  color: var(--st-gray-text-color, #718096);
}
.dcb-title-fit {
  margin: 0 0 0.35rem 0;
  padding: 0;
  font-weight: 600;
  line-height: 1.2;
  word-break: normal !important;
  overflow-wrap: normal !important;
  hyphens: none;
  color: var(--st-heading-color, var(--st-text-color, #31333F));
  font-size: 1.2rem;
}
@supports (font-size: 1cqi) {
  .dcb-title-fit {
    container-type: inline-size;
    font-size: max(0.8rem, min(1.35rem, calc(100cqi / (var(--label-chars, 8) * 0.45))));
  }
}
/* Missing asset: initials tile uses theme colors (fixed slate looked wrong in dark mode). */
.dcb-icon-fallback-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  font-weight: 700;
  background: var(--st-secondary-background-color);
  color: var(--st-text-color);
  border: 1px solid var(--st-border-color);
  border-radius: var(--st-base-radius, 0.625rem);
}
</style>
""",
        unsafe_allow_html=True,
    )


def _purchased_item_button_key(item_name: str) -> str:
    digest = hashlib.sha256(item_name.encode("utf-8")).hexdigest()[:16]
    return f"purch_rm_{digest}"


def _recommendation_add_button_key(item_name: str) -> str:
    digest = hashlib.sha256(item_name.encode("utf-8")).hexdigest()[:16]
    return f"rec_add_{digest}"


def _selected_enemy_toggle_key(hero_idx: int, row_start: int, slot: int, item_name: str) -> str:
    digest = hashlib.sha256(item_name.encode("utf-8")).hexdigest()[:12]
    return f"se_toggle_{hero_idx}_{row_start}_{slot}_{digest}"


def add_purchased_item(item_name: str) -> None:
    if item_name in _ITEMS_EXCLUDED_FROM_PURCHASED:
        return
    cur = list(st.session_state.get("purchased_items", []))
    if item_name in cur:
        return
    if len(cur) >= MAX_PURCHASED_ITEMS:
        return
    cur.append(item_name)
    st.session_state.purchased_items = cur


def sell_purchased_item(item_name: str) -> None:
    cur = list(st.session_state.get("purchased_items", []))
    st.session_state.purchased_items = [x for x in cur if x != item_name]


@st.cache_data
def get_game_data_cached(path_str: str) -> dict:
    return load_game_data(path_str)


@st.cache_data
def get_item_icon_index_cached(root_str: str) -> dict[str, str]:
    return build_categorized_item_icon_index(Path(root_str))


def _label_fit_longest_token_len(text: str) -> int:
    """Length of longest whitespace-delimited segment; used to size text so one word fits."""
    parts = text.split()
    if not parts:
        return 1
    return max(len(p) for p in parts)


def render_icon_caption_label(text: str) -> None:
    """Caption under a narrow icon tile: scales down long names; wraps only between words."""
    metric = _label_fit_longest_token_len(text)
    escaped = html.escape(text)
    st.markdown(
        f'<div class="dcb-label-fit" style="--label-chars:{metric}">{escaped}</div>',
        unsafe_allow_html=True,
    )


def render_card_title_label(text: str) -> None:
    """Item title in recommendation cards; same word rules with a larger type scale."""
    metric = _label_fit_longest_token_len(text)
    escaped = html.escape(text)
    st.markdown(
        f'<p class="dcb-title-fit" style="--label-chars:{metric}">{escaped}</p>',
        unsafe_allow_html=True,
    )


def render_image_or_fallback(
    *,
    rel_path: str,
    fallback_text: str,
    width: int,
    greyed_out: bool = False,
) -> None:
    """Show a local image if it exists under the project root; otherwise a compact text badge.

    Icons are embedded at full file resolution and sized with CSS ``width`` (not the HTML
    ``width`` attribute) so HiDPI displays can sample enough pixels instead of upscaling a
    small bitmap produced by fixed-pixel image APIs.
    """
    resolved = resolve_asset_path(PROJECT_ROOT, rel_path)
    if resolved is not None:
        mime, b64 = _cached_asset_data_uri((str(resolved), resolved.stat().st_mtime))
        safe_title = html.escape(fallback_text, quote=True)
        safe_alt = safe_title
        filter_style = "opacity:0.42;filter:grayscale(1);" if greyed_out else ""
        st.markdown(
            f'<img src="data:{mime};base64,{b64}" alt="{safe_alt}" title="{safe_title}" '
            f'style="{filter_style}width:{width}px;height:auto;max-width:{width}px;'
            'display:block;" />',
            unsafe_allow_html=True,
        )
        return

    initials = "".join(part[0] for part in fallback_text.split()[:2] if part).upper() or "?"
    safe_title = html.escape(fallback_text, quote=True)
    dim = "opacity:0.42;filter:grayscale(1);" if greyed_out else ""
    st.markdown(
        f'<div class="dcb-icon-fallback-badge" title="{safe_title}" style="{dim}'
        f"width:{width}px;min-height:{width}px;max-height:{width}px;"
        f'font-size:{max(11, width // 5)}px;">{initials}</div>',
        unsafe_allow_html=True,
    )


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


def render_recommendations(
    selected: list[str],
    game_data: dict,
    item_icon_index: dict[str, str],
    *,
    exclude_items: Collection[str] | None = None,
) -> None:
    skip = frozenset(exclude_items or ())
    all_rows = recommend_items(selected, game_data)
    candidates = [r for r in all_rows if r["item"] not in skip]
    rows = [r for r in candidates if r["coverage_count"] > 1]

    st.subheader("Recommended counter items")
    st.caption(
        "Sorted by how many of your selected enemies each item counters. "
    )

    if not rows:
        if not all_rows:
            st.info("No counter items were found for the current selection.")
        elif not candidates:
            st.info(
                "No counter items left to show — try removing some items from **Already owned**, "
                "or your selection may not share any remaining counters."
            )
        else:
            st.info(
                "No items counter more than one of your selected enemies. "
                "See **Selected Enemies** for per-hero counter items."
            )
        return

    def render_one_recommendation_card(row: dict) -> None:
        coverage = row["coverage_count"]
        item_name = row["item"]
        countered = row["countered_heroes"]

        item_rel = item_icon_path(
            game_data,
            item_name,
            project_root=PROJECT_ROOT,
            categorized_index=item_icon_index,
        )

        head_key = f"dcb_rh_{hashlib.sha256(item_name.encode('utf-8')).hexdigest()[:12]}"
        with st.container(border=True):
            with st.container(key=head_key):
                at_owned_cap = (
                    len(st.session_state.get("purchased_items", [])) >= MAX_PURCHASED_ITEMS
                )
                # Icon | rationale (name + coverage) | Buy — one row, no tall icon+button rail.
                head = st.columns([0.14, 0.66, 0.20], gap="small")
                with head[0]:
                    render_image_or_fallback(
                        rel_path=item_rel,
                        fallback_text=item_name,
                        width=ITEM_ICON_WIDTH,
                    )
                with head[1]:
                    render_card_title_label(item_name)
                    st.markdown(
                        f"**Counters {coverage} enemies**"
                    )
                with head[2]:
                    st.button(
                        "Buy",
                        key=_recommendation_add_button_key(item_name),
                        on_click=add_purchased_item,
                        args=(item_name,),
                        type="secondary",
                        use_container_width=True,
                        disabled=at_owned_cap,
                    )

            render_countered_heroes_chips(game_data, countered)
            st.markdown(
                '<div style="height:0.45rem;" aria-hidden="true"></div>',
                unsafe_allow_html=True,
            )

    for row_start in range(0, len(rows), 2):
        pair = rows[row_start : row_start + 2]
        with st.container(key=f"dcb_rec_pair_{row_start}"):
            cols = st.columns(2, gap="medium")
            for col, row in zip(cols, pair):
                with col:
                    render_one_recommendation_card(row)


def render_purchased_items_panel(game_data: dict, item_icon_index: dict[str, str]) -> None:
    """Let the player mark items they already bought; those are hidden from recommendations."""
    st.subheader("Purchased items")

    all_item_names = sorted(game_data["items"].keys())
    if "purchased_items" not in st.session_state:
        st.session_state.purchased_items = []
    else:
        cleaned = [x for x in st.session_state.purchased_items if x not in _ITEMS_EXCLUDED_FROM_PURCHASED]
        capped = cleaned[:MAX_PURCHASED_ITEMS]
        if capped != st.session_state.purchased_items:
            st.session_state.purchased_items = list(capped)

    purchasable_item_names = [n for n in all_item_names if n not in _ITEMS_EXCLUDED_FROM_PURCHASED]

    st.multiselect(
        "Items you already bought",
        options=purchasable_item_names,
        key="purchased_items",
        max_selections=MAX_PURCHASED_ITEMS,
        placeholder="Add items you already own…",
        help=(
            f"Up to {MAX_PURCHASED_ITEMS} owned items. "
            "Selected items use icons from assets/items when available."
        ),
    )

    purchased: list[str] = list(st.session_state.get("purchased_items", []))
    if not purchased:
        st.caption("No items marked yet — recommendations show every counter item.")
        return

    st.markdown("**Owned items**")
    for row_start in range(0, len(purchased), PURCHASED_ITEMS_ICONS_PER_ROW):
        chunk = purchased[row_start : row_start + PURCHASED_ITEMS_ICONS_PER_ROW]
        cols = st.columns(len(chunk), gap="small")
        for col, item_name in zip(cols, chunk):
            with col:
                item_rel = item_icon_path(
                    game_data,
                    item_name,
                    project_root=PROJECT_ROOT,
                    categorized_index=item_icon_index,
                )
                render_image_or_fallback(
                    rel_path=item_rel,
                    fallback_text=item_name,
                    width=PURCHASED_ITEM_ICON_WIDTH,
                )
                st.button(
                    "Sell",
                    key=_purchased_item_button_key(item_name),
                    on_click=sell_purchased_item,
                    args=(item_name,),
                    type="secondary",
                )


def render_selected_enemies_counter_lists(
    selected: list[str],
    game_data: dict,
    item_icon_index: dict[str, str],
    *,
    purchased_items: Collection[str] | None = None,
) -> None:
    owned = frozenset(purchased_items or ())
    st.markdown("##### Selected Enemies")
    if not selected:
        st.caption("Pick up to 6 heroes from the list above.")
        return

    for i, hero_name in enumerate(selected):
        items = counter_items_for_hero(game_data, hero_name)
        cur_purchased = list(st.session_state.get("purchased_items", []))
        at_owned_cap = len(cur_purchased) >= MAX_PURCHASED_ITEMS
        with st.container(key=f"dcb_hero_row_{i}"):
            sub = st.columns([0.14, 0.86], gap="small")
            with sub[0]:
                render_image_or_fallback(
                    rel_path=hero_icon_path(game_data, hero_name),
                    fallback_text=hero_name,
                    width=HERO_ICON_WIDTH,
                )
                render_icon_caption_label(hero_name)
            with sub[1]:
                with st.container(key=f"dcb_hero_items_{i}"):
                    if items:
                        for row_start in range(
                            0, len(items), SELECTED_ENEMY_ITEM_ICONS_PER_ROW
                        ):
                            chunk = items[
                                row_start : row_start + SELECTED_ENEMY_ITEM_ICONS_PER_ROW
                            ]
                            cols = st.columns(len(chunk), gap="small")
                            for slot, (col, it) in enumerate(zip(cols, chunk)):
                                with col:
                                    render_image_or_fallback(
                                        rel_path=item_icon_path(
                                            game_data,
                                            it,
                                            project_root=PROJECT_ROOT,
                                            categorized_index=item_icon_index,
                                        ),
                                        fallback_text=it,
                                        width=PER_HERO_ITEM_ICON_WIDTH,
                                        greyed_out=it in owned,
                                    )
                                    owned_here = it in owned
                                    excluded = it in _ITEMS_EXCLUDED_FROM_PURCHASED
                                    toggle_key = _selected_enemy_toggle_key(i, row_start, slot, it)
                                    if owned_here:
                                        st.button(
                                            "Sell",
                                            key=toggle_key,
                                            on_click=sell_purchased_item,
                                            args=(it,),
                                            type="secondary",
                                            use_container_width=True,
                                        )
                                    else:
                                        buy_disabled = excluded or (
                                            at_owned_cap and it not in cur_purchased
                                        )
                                        st.button(
                                            "Buy",
                                            key=toggle_key,
                                            on_click=add_purchased_item,
                                            args=(it,),
                                            type="secondary",
                                            use_container_width=True,
                                            disabled=buy_disabled,
                                        )
                    else:
                        st.caption("No items listed for this hero.")
        if i < len(selected) - 1:
            st.divider()


def main() -> None:
    st.set_page_config(page_title="Deadlock Counter Builder", page_icon="🎯", layout="wide")
    inject_responsive_css()

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

    item_icon_index = get_item_icon_index_cached(str(PROJECT_ROOT))
    all_heroes = sorted_hero_names(game_data)
    purchased_set = frozenset(st.session_state.get("purchased_items", []))

    with st.container(key="dcb_main_split"):
        left, right = st.columns([1, 1.35], gap="large")

    with left:
        st.subheader("Enemy gamers")

        with st.container(key="dcb_enemy_pick_row"):
            selected = st.multiselect(
                "Choose enemy heroes",
                options=all_heroes,
                default=st.session_state.get("enemy_selection", []),
                max_selections=MAX_SELECTIONS,
                key="enemy_selection",
                placeholder="Type to filter heroes…",
                help=f"Select exactly {MAX_SELECTIONS} heroes to unlock ranked items.",
            )

        render_selected_enemies_counter_lists(
            selected,
            game_data,
            item_icon_index,
            purchased_items=purchased_set,
        )

        if len(selected) < MAX_SELECTIONS:
            st.info(f"Choose **{MAX_SELECTIONS - len(selected)}** more hero(es) to see recommendations.")

    with right:
        render_purchased_items_panel(game_data, item_icon_index)

        if len(selected) == MAX_SELECTIONS:
            render_recommendations(
                selected,
                game_data,
                item_icon_index,
                exclude_items=purchased_set,
            )
        else:
            st.subheader("Recommended counter items")
            st.info(
                f"Recommendations unlock when **{MAX_SELECTIONS}** enemies are selected. "
                "Use the panel on the left to finish your pick."
            )


if __name__ == "__main__":
    main()
