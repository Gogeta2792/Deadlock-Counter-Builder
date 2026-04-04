Item icon files (local images)
==============================

Each item name in data/character_counters.json has a matching entry under "items" with an "icon"
path. Paths are relative to the project root.

Suggested naming (easy to maintain)
-----------------------------------
Use lowercase with underscores, derived from the display name:

  Display name      -> suggested file
  Knockdown         -> assets/items/knockdown.png
  Slowing Hex       -> assets/items/slowing_hex.png
  Spirit Shielding  -> assets/items/spirit_shielding.png

The JSON already lists expected paths for every item. Add PNG (or JPG) files here with those
exact names, or edit the "icon" string in JSON to point at your file.

Sample placeholders in JSON
---------------------------
Two example-only items are included at the bottom of the "items" section:
  (Example) New Item Alpha  -> assets/items/example_new_item_alpha.png
  (Example) New Item Beta   -> assets/items/example_new_item_beta.png

They are not assigned to any hero until you wire them into a hero's "counter_items" list.

If a file is missing, the UI shows initials in a small tile instead of crashing.
