# Birds of Paradise — desktop theme collection

Personal Linux desktop theming, anchored to the [gerane "Birds of Paradise" VS Code](https://github.com/gerane/VSCode-Theme-BirdsOfParadise) tmTheme palette. Warm dark browns, cream foreground, amber accents, magenta selection.

## Components

| Component | Status | Path |
|---|---|---|
| GNOME Shell theme | ✅ shipped | [`gnome-shell/`](./gnome-shell) |
| Firefox theme (.xpi) | ✅ shipped | [`firefox/`](./firefox) |
| GNOME Terminal palette | ✅ shipped | [`terminal/`](./terminal) |
| GTK 3/4 theme + libadwaita overrides | planned | `gtk/` |
| GRUB theme | planned | `grub/` |

## Palette (source of truth)

From `gerane.theme-birdsofparadise` VS Code extension `Birds_of_Paradise.tmTheme`:

| Hex | Role |
|---|---|
| `#372725` | bg |
| `#2E211F` | bg (one-step-darker chrome) |
| `#2A1C1B` | popovers |
| `#1F1413` | deepest borders / panel |
| `#E6E1C4` | fg |
| `#FFF9D5` / `#F8F8F8` | bright white |
| `#EFAC32` | accent gold (entity) |
| `#F1B64A` | amber light |
| `#C5850F` | amber dark (active button bg) |
| `#EF5D32` | orange-red (keyword) |
| `#A40042` | **iconic magenta** (selection) |
| `#7DAF9C` | sage (variable / success) |
| `#6C99BB` | blue (constant) |
| `#BE73FD` | purple (regexp) |
| `#86B4BB` | teal (xml tag) |
| `#AFC4DB` | light slate (preprocessor) |
| `#D9D762` | yellow (string) |
| `#6B4E32` | comment / muted |
| `#CC4232` | invalid / error |

## Target environment

- Ubuntu 24.04, GNOME 46, Wayland session
- ThinkPad
