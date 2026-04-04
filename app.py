"""Streamlit app for Deadlock counter item recommendations."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.recommender import (
    DataValidationError,
    load_character_counters,
    recommend_items,
)

DATA_PATH = Path("data/character_counters.json")
MAX_SELECTIONS = 6


@st.cache_data
def get_data(path: str) -> dict:
    return load_character_counters(path)


def reset_selection() -> None:
    st.session_state["enemy_selection"] = []


def render_recommendations(selected_characters: list[str], character_counters: dict) -> None:
    recommendations = recommend_items(selected_characters, character_counters)

    st.subheader("Recommended Counter Items")

    if not recommendations:
        st.info("No recommendations were generated for the current selection.")
        return

    for row in recommendations:
        coverage = row["coverage_count"]
        item = row["item"]
        covered_chars = ", ".join(row["countered_characters"])
        ratio = coverage / MAX_SELECTIONS

        if coverage >= 5:
            strength_label = "🔥 Strongest Overall Counter"
        elif coverage >= 3:
            strength_label = "✅ Good Coverage"
        else:
            strength_label = "ℹ️ Situational"

        with st.container(border=True):
            st.markdown(f"### {item}")
            st.markdown(f"**Counters {coverage}/{MAX_SELECTIONS} selected characters**")
            st.progress(ratio)
            st.caption(strength_label)
            with st.expander("See which selected characters this item counters"):
                st.write(covered_chars)


def render_character_details(selected_characters: list[str], character_counters: dict) -> None:
    with st.expander("Selected Characters and Their Counter Items", expanded=False):
        for character in selected_characters:
            items = character_counters.get(character, [])
            st.markdown(f"**{character}**")
            if items:
                st.write(", ".join(items))
            else:
                st.caption("No items listed for this character in the dataset.")


def main() -> None:
    st.set_page_config(page_title="Deadlock Counter Builder", page_icon="🎯", layout="wide")

    st.title("🎯 Deadlock Counter Builder")
    st.write(
        "Select exactly 6 enemy characters and get item recommendations ranked by coverage."
    )

    try:
        character_counters = get_data(str(DATA_PATH))
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()
    except DataValidationError as error:
        st.error(f"Data validation error: {error}")
        st.stop()
    except Exception as error:  # noqa: BLE001
        st.error(f"Unexpected error while loading data: {error}")
        st.stop()

    all_characters = sorted(character_counters.keys())

    col_left, col_right = st.columns([1, 1.4], gap="large")

    with col_left:
        st.subheader("Enemy Character Selection")
        st.caption("Search and choose 6 unique enemy characters.")

        selected_characters = st.multiselect(
            "Choose enemy characters",
            options=all_characters,
            default=st.session_state.get("enemy_selection", []),
            max_selections=MAX_SELECTIONS,
            key="enemy_selection",
            placeholder="Type to search characters...",
            help="You must select exactly 6 characters to generate recommendations.",
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.metric("Selected", f"{len(selected_characters)}/{MAX_SELECTIONS}")
        with col_b:
            st.button("Reset selections", on_click=reset_selection, type="secondary")

        if len(selected_characters) < MAX_SELECTIONS:
            st.info("Select 6 characters to see ranked recommendations.")
        elif len(selected_characters) > MAX_SELECTIONS:
            st.warning("Please select only 6 characters.")

        if len(selected_characters) == MAX_SELECTIONS:
            render_character_details(selected_characters, character_counters)

    with col_right:
        if len(selected_characters) == MAX_SELECTIONS:
            render_recommendations(selected_characters, character_counters)
        else:
            st.subheader("Recommended Counter Items")
            st.info("Recommendations will appear here once exactly 6 enemies are selected.")


if __name__ == "__main__":
    main()
