# Deadlock Counter Builder (Streamlit)

A beginner-friendly local Streamlit app that recommends counter-items based on 6 selected enemy characters and a JSON dataset you control.

## Why this architecture?

This project is intentionally simple and easy to edit:

- **Streamlit for UI**: fast to build, no frontend framework needed, built-in searchable selection and reactive updates.
- **JSON for data**: human-readable and easy to maintain; you can update counters without touching Python logic.
- **Modular Python**:
  - `utils/recommender.py` handles data loading/validation and recommendation logic.
  - `app.py` handles UI only.

This separation makes it easier to maintain and customize.

## Project structure

```text
.
├── app.py
├── data/
│   └── character_counters.json
├── utils/
│   └── recommender.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## Data format and editing

Edit `data/character_counters.json`.

Expected shape:

```json
{
  "Character Name": ["Counter Item 1", "Counter Item 2", "Counter Item 3"],
  "Another Character": ["Counter Item 2", "Counter Item 4"]
}
```

Rules:

- Each key is a character name.
- Each value is a list of item names.
- Duplicate items under the same character are automatically de-duplicated.

## Recommendation logic

Given exactly 6 selected enemy characters, the app:

1. Loads each character's counter item list from JSON.
2. Counts item frequency across selected characters (simple frequency count).
3. Builds a mapping of `item -> selected characters it counters`.
4. Sorts results by:
   - highest coverage count first,
   - then alphabetical item name for stable ties.
5. Displays each item with:
   - item name,
   - coverage as `X/6`,
   - which selected characters it counters.

## UI behavior

- Searchable enemy character selection using Streamlit multiselect.
- Requires **exactly 6** selected characters to show recommendations.
- Reset button to clear selections.
- Secondary expandable panel shows selected characters and each character's listed counter items.
- Visual emphasis for strongest counters using coverage labels and progress bars.

## Error handling

- Missing JSON file: clear error message in the app.
- Malformed JSON structure: validation error shown in the app.

