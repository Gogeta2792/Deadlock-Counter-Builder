Hero portrait files (local images)
==================================

The app loads paths listed under each hero in data/character_counters.json (field "icon").
Paths are relative to the project root (the folder that contains app.py).

Naming convention (matches common Deadlock wiki exports)
----------------------------------------------------------
  132px-<HeroName>_card.png

Rules:
  - Replace spaces in the hero name with underscores.
  - Keep "&" as "&" (example: Mo & Krill -> 132px-Mo_&_Krill_card.png).
  - Case-sensitive on disk; match the spelling in JSON.

Examples:
  - Abrams        -> assets/heroes/132px-Abrams_card.png
  - Grey Talon    -> assets/heroes/132px-Grey_Talon_card.png
  - Lady Geist    -> assets/heroes/132px-Lady_Geist_card.png

If the file is missing, the UI shows a text badge with initials instead of crashing.
