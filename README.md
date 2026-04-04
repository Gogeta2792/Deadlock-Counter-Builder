# Deadlock Counter Builder (Streamlit)

A small, local Streamlit app that ranks **counter items** after you pick **six** enemy heroes. Data based on various community data; images live under `assets/`. The recommendation math stays in plain Python so the UI stays easy to change.

## Why this layout?

- **Streamlit** gives a searchable multiselect and quick layout without a separate frontend. Multiselect rows cannot show images, so the app lists **names** in the widget and shows **icons in a panel below** (a common, maintainable workaround).
- **`utils/data_loader.py`** loads and validates JSON, resolves icon paths safely under the project root, and exposes small helpers (`hero_icon_path`, `item_icon_path`, etc.).
- **`utils/recommender.py`** only ranks items from selected heroes—no file I/O, no UI imports—so you can test or reuse it easily.
- **`app.py`** handles layout, images, and fallbacks when files are missing.

## Project structure

```text
.
├── app.py                      # Streamlit UI only
├── data/
│   └── character_counters.json # Heroes, per-hero counter lists, item icon paths
├── assets/
│   ├── heroes/                 # Hero card images (see assets/heroes/README.txt)
│   └── items/                  # Item icons (see assets/items/README.txt)
├── utils/
│   ├── data_loader.py          # Load JSON, validate, resolve asset paths
│   └── recommender.py          # Coverage counting and sorting
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## Data format (`data/character_counters.json`)

Top-level object with **`heroes`** and **`items`**:

```json
{
  "heroes": {
    "Abrams": {
      "icon": "assets/heroes/132px-Abrams_card.png",
      "counter_items": ["Slowing Hex", "Reactive Barrier"]
    }
  },
  "items": {
    "Slowing Hex": {
      "icon": "assets/items/slowing_hex.png"
    }
  }
}
```

Rules:

- **Hero keys** are the exact names shown in the multiselect.
- **`counter_items`** lists item **display names**; each name should also exist under **`items`** (optional but recommended for icons).
- **`icon`** values are paths **relative to the project root**. Missing files do not crash the app; you get a text badge with initials instead.

The file also includes two **example-only** items at the bottom of `items` (names prefixed with `(Example)`) so you can copy the pattern when adding real items later.

## Naming image files so the app finds them

- **Heroes:** see `assets/heroes/README.txt` (pattern `132px-<Name_with_underscores>_card.png`).
- **Items:** see `assets/items/README.txt` (lowercase `snake_case.png` matching the `"icon"` field in JSON).

The app resolves paths with `pathlib`, checks that the file exists, and ensures the path does not escape the project folder with `..`.

## How to add a new hero

1. Add a PNG under `assets/heroes/` using the naming rules in `assets/heroes/README.txt`.
2. In `character_counters.json`, under `heroes`, add:

```json
"New Hero": {
  "icon": "assets/heroes/132px-New_Hero_card.png",
  "counter_items": ["Knockdown", "Healbane"]
}
```

3. Under `items`, ensure each counter item has an entry with an `icon` path (copy an existing block and change names/paths).

## How to add a new item

1. Pick a **display name** (what players see). Add a file under `assets/items/`, e.g. `my_new_item.png`.
2. In `items`:

```json
"My New Item": {
  "icon": "assets/items/my_new_item.png"
}
```

3. Reference that exact display name in one or more heroes’ `counter_items` arrays.

## Recommendation logic

When exactly **six** heroes are selected:

1. For each selected hero, read `counter_items` from `heroes`.
2. For each item name, collect which selected heroes list that item (set semantics per hero—duplicates in JSON are already removed on load).
3. Sort items by **highest coverage count first**, then **alphabetical** item name.
4. The UI shows item name, icon (or fallback), **coverage `X/6`**, a progress bar, and which selected heroes are covered.

## UI notes

- **Enemy roster:** multiselect (text only) + **Selected enemies** grid with icons.
- **Recommendations:** bordered cards with item icon, title, coverage text, progress bar, and a row of covered hero icons.
- **Per-hero counter lists:** expandable section with hero portrait and each counter item with its icon.

## Error handling

- Missing JSON file or invalid structure: clear message in the app (`DataValidationError` from `data_loader`).
- Missing image: initials badge; no crash.
