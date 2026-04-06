# UI element reference

This document gives **stable names** for every user-visible piece of the Streamlit UI so you can refer to them in issues, PRs, and code reviews without ambiguity. All elements are defined in [`app.py`](app.py) unless noted.

## Page shell

| Canonical name | What it is | In code |
| --- | --- | --- |
| **Browser tab title** | Document title shown in the browser tab | `st.set_page_config(..., page_title="Deadlock Counter Builder", ...)` |
| **Page icon** | Favicon (emoji) for the tab | `page_icon="🎯"` in `st.set_page_config` |
| **Wide layout** | Full-width app layout | `layout="wide"` in `st.set_page_config` |

## Global header (full width)

| Canonical name | What it is | In code |
| --- | --- | --- |
| **App title** | Main heading at the top of the page | `st.title("Deadlock Counter Builder")` |
| **Intro blurb** | Short instructions under the title | `st.write("Select **6** enemy heroes. ...")` |

## Error banners (full width, on load failure)

| Canonical name | When it appears | In code |
| --- | --- | --- |
| **Missing data file error** | JSON path missing | `st.error(str(err))` after `FileNotFoundError` |
| **Data validation error** | JSON fails schema/validation | `st.error(f"Data validation error: {err}")` |
| **Unexpected load error** | Any other exception while loading data | `st.error(f"Unexpected error while loading data: {err}")` |

## Main two-column layout

| Canonical name | Role | In code |
| --- | --- | --- |
| **Left column** | Enemy selection, metrics, selected roster, optional per-hero breakdown | `left, right = st.columns([1, 1.35], ...)` → `with left:` |
| **Right column** | Recommendations (or placeholder until six heroes are picked) | `with right:` |

---

## Left column — enemy selection region

| Canonical name | What it is | Streamlit / state | In code |
| --- | --- | --- | --- |
| **Enemy section heading** | Subheader above the picker | `st.subheader` | Label: `"Enemy gamers"` |
| **Enemy hero multiselect** | Searchable list to pick up to six enemy heroes | Widget label `"Choose enemy heroes"`; **`key="enemy_selection"`** (also session state key) | `st.multiselect(...)` |
| **Selection count metric** | Shows `N / 6` selected | Metric label `"Selected"` | `st.metric("Selected", ...)` |
| **Clear selection button** | Resets the multiselect via callback | `st.button("Clear selection", on_click=reset_selection, type="secondary")` | Triggers `reset_selection` → clears `st.session_state["enemy_selection"]` |
| **Selected enemies heading** | Small heading above the icon grid | Markdown level-5 | `st.markdown("##### Selected enemies")` inside `render_selected_heroes_panel` |
| **Selected enemies empty hint** | Caption when nobody is selected | — | `st.caption("Pick up to 6 heroes from the list above.")` |
| **Selected enemy tile** | One cell: hero portrait (or initials badge) + bold name | Built from nested columns | `render_hero_row` → `render_image_or_fallback` + `st.markdown(f"**{hero_name}**")` |
| **Selected enemies grid** | Up to three tiles per row for current selection | — | `render_selected_heroes_panel` loops `st.columns` in chunks of 3 |
| **Progress info callout** | Blue info when fewer than six heroes selected | Dynamic count in message | `st.info(f"Choose **{...}** more hero(es) to see recommendations.")` |
| **Per-hero counter lists (expander)** | Collapsible section listing each picked hero and their counter items with icons | Expander title `"Per-hero counter lists"` | `st.expander(..., expanded=False)` in `render_per_hero_breakdown` |
| **Per-hero row** | Hero portrait + name + row of item icons | — | Loop in `render_per_hero_breakdown` |
| **Per-hero item icon cell** | Small item icon + caption under a hero | — | `render_image_or_fallback` (width 36) + `st.caption(it)` |
| **Per-hero empty items caption** | Shown when a hero has no `counter_items` | — | `st.caption("No items listed for this hero.")` |

---

## Right column — recommendations region

| Canonical name | What it is | When shown | In code |
| --- | --- | --- | --- |
| **Recommendations section heading** | Subheader above the list or placeholder | Always in this column (either above cards or above placeholder) | `"Recommended counter items"` via `st.subheader` in `render_recommendations` **or** in `main` when waiting for six picks |
| **Recommendations locked callout** | Info explaining that six enemies are required | Fewer than six selected | `st.info(...)` in `main` under right column |
| **Recommendations sort caption** | Explains sort order | Exactly six selected and recommendations render | `st.caption("Sorted by how many of your selected enemies each item counters.")` |
| **No recommendations info** | Info when the ranked list is empty | Six selected but `recommend_items` returns nothing | `st.info("No counter items were found for the current selection.")` |
| **Recommendation card** | Bordered container for one ranked item | One per recommended item | `st.container(border=True)` in `render_recommendations` |
| **Recommendation card — item icon** | Item artwork or initials badge | Inside card header row | `render_image_or_fallback` with `ITEM_ICON_WIDTH` |
| **Recommendation card — item title** | Item name as a heading | — | `st.markdown(f"### {item_name}")` |
| **Recommendation card — coverage summary** | Text: counters count + strength label (*Strong coverage* / *Solid pick* / *Situational*) | — | `st.markdown(f"**Counters {coverage}/{n} selected heroes** — _{strength}_")` |
| **Recommendation card — coverage progress bar** | Visual fraction of roster covered | — | `st.progress(ratio, text=...)` |
| **Recommendation card — coverage metric** | Numeric `coverage / n` with tooltip | Metric label `"Coverage"` | `st.metric("Coverage", ..., help="How many of your selected enemies this item counters.")` |
| **Recommendation card — covered heroes heading** | Label above the chip row | — | `st.markdown("**Covered heroes**")` |
| **Covered hero chip** | Small hero icon + caption for one countered enemy | — | `render_countered_heroes_chips` |
| **Covered heroes empty caption** | When an item covers none of the six | — | `st.caption("None of the selected heroes.")` |

---

## Visual fallbacks (not separate widgets)

| Canonical name | Role | In code |
| --- | --- | --- |
| **Image or initials badge** | Shows a local image if the asset exists; otherwise a styled HTML badge with initials | `render_image_or_fallback` |
| **Initials badge** | Gray rounded box with 1–2 letters when image missing | Built in `render_image_or_fallback` via `st.markdown(..., unsafe_allow_html=True)` |

---

## Constants that affect the UI

| Name | Meaning | Value / location |
| --- | --- | --- |
| `MAX_SELECTIONS` | Required enemy count to unlock recommendations | `6` |
| `HERO_ICON_WIDTH` | Pixel width for hero images in main panels | `56` |
| `ITEM_ICON_WIDTH` | Pixel width for item images on recommendation cards | `52` |
| `PER_HERO_ITEM_ICONS_PER_ROW` | Max item icons per row inside per-hero expander | `10` |

---

## Session state

| Key | Used by | Purpose |
| --- | --- | --- |
| `enemy_selection` | Multiselect `key=` and `reset_selection` | Persists/clears the selected enemy hero names |

---

## Related modules (no direct Streamlit UI)

| Module | Role |
| --- | --- |
| [`utils/data_loader.py`](utils/data_loader.py) | Load JSON, resolve asset paths, hero/item helpers |
| [`utils/recommender.py`](utils/recommender.py) | Rank items for the **Recommendation card** list |

When you add or rename a widget, update this file in the same change so names stay in sync with `app.py`.
