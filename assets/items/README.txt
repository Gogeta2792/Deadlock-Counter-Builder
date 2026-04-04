Item icon files (local images)
==============================

Icons are organized by item category for maintenance:

  assets/items/Spirit/    — spirit-slot items
  assets/items/Weapon/  — weapon-slot items
  assets/items/Vitality/ — vitality-slot items

Each item name in data/character_counters.json is matched to a file by normalizing the
display name and the image filename the same way: lowercase letters and digits only
(spaces and punctuation stripped). Examples:

  "Spirit Sap"     matches  Spirit/Spirit Sap.png  or  Spirit/SpiritSap.png
  "Crippling Headshot"  matches  Weapon/CripplingHeadshot.png

The optional "icon" field under each item in JSON is still tried first. If that path is
missing, the app looks up the categorized folders above.

Supported extensions: .png, .jpg, .jpeg, .webp

If no file matches, the UI shows initials in a small tile instead of crashing.

Sample placeholders in JSON
---------------------------
Two example-only items at the bottom of the "items" section are not assigned to any hero
until you wire them into a hero's "counter_items" list.
