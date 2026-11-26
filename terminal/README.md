# Birds of Paradise — GNOME Terminal profile

A 16-color ANSI palette + bg/fg/cursor/highlight set for GNOME Terminal, mapped to the BoP tmTheme palette.

## Install

```
./install.sh
```

This loads the profile under UUID `aca24da3-722c-4f53-b35f-9832234b46f7`, registers it in `profiles:/list` (idempotent), and sets it as the default profile. New terminal windows pick it up immediately; existing windows show the new colors after you change profile (right-click → Profiles) or close and reopen.

## Update (after editing the profile in GNOME Terminal Preferences)

```
dconf dump /org/gnome/terminal/legacy/profiles:/:aca24da3-722c-4f53-b35f-9832234b46f7/ > birds-of-paradise.dconf
```

Then commit the diff.

## File format

The dump uses `dconf`'s INI-style serialization. Colors are stored in **16-bit per channel** form (`#RRRRGGGGBBBB`) — the same color in 8-bit (`#RRGGBB`) is just doubled (e.g., `#372725` becomes `#373727272525`). GNOME Terminal historically supported deep-color displays; modern GTK still uses this format for the dconf store.

## Color map (8-bit form, BoP roles)

**Surface:**

| Slot | Hex | Role |
|---|---|---|
| `background-color` | `#372725` | bg |
| `foreground-color` | `#E6E1C4` | fg |
| `bold-color` | `#EFB732` | custom: warm gold |
| `cursor-background-color` | `#A40042` | custom: iconic magenta, same as selection |
| `cursor-foreground-color` | `#372725` | text under cursor |
| `highlight-background-color` | `#A40042` | iconic magenta selection |
| `highlight-foreground-color` | `#FFF9D5` | warm white on magenta |

**ANSI palette (0–15):**

| # | Name | Hex | tmTheme role |
|---|---|---|---|
| 0 | Black | `#1F1413` | deepest border |
| 1 | Red | `#CC4232` | invalid |
| 2 | Green | `#7DAF9C` | sage / variable |
| 3 | Yellow | `#EFAC32` | accent gold |
| 4 | Blue | `#6C99BB` | constant |
| 5 | Magenta | `#FF9928` | custom: amber |
| 6 | Cyan | `#86B4BB` | xml tag |
| 7 | White | `#E6E1C4` | foreground cream |
| 8 | Bright Black | `#5B413D` | muted brown |
| 9 | Bright Red | `#EF5D32` | keyword orange-red |
| 10 | Bright Green | `#19E7BB` | custom: aqua |
| 11 | Bright Yellow | `#3FD72C` | custom: green |
| 12 | Bright Blue | `#0000FF` | custom: pure blue |
| 13 | Bright Magenta | `#FF9930` | custom: amber |
| 14 | Bright Cyan | `#C2294D` | custom: crimson |
| 15 | Bright White | `#F8F8F8` | bright |
