# Birds of Paradise — herdr theme

[herdr](https://herdr.dev) is a terminal workspace manager. It paints its own chrome in
truecolor: tab bar, sidebar, pane borders, status line, popups. This is that chrome in BoP.

It colours nothing the shell prints — that is the terminal emulator's palette. Pair this with
[`terminal/`](../terminal) on GNOME or [`terminal-app/`](../terminal-app) on macOS.

## Install

herdr has no theme directory to drop a file into: the theme lives in the config. Copy the
`[theme]` and `[theme.custom]` blocks from `birds-of-paradise.toml` into
`~/.config/herdr/config.toml`, replacing whatever is there, then:

```
cp ~/.config/herdr/config.toml ~/.config/herdr/config.toml.bak.$(date +%Y%m%d-%H%M%S)
herdr server reload-config
```

Back up first — the config holds keybindings and plugin state alongside the theme, and this
file is only the theme half of it.

`name = "catppuccin"` stays. It selects the base theme whose slots `[theme.custom]` overrides;
the overrides are what render. Removing the base leaves any slot this file does not name
unthemed.

## Slots

Names are catppuccin's, because that is the vocabulary herdr's config uses. The mapping
follows BoP's semantics.

| Slot | Hex | Role |
|---|---|---|
| `panel_bg` | `#372725` | bg |
| `sidebar_bg` | `#2E211F` | bg, one step darker — chrome |
| `surface_dim` | `#1F1413` | deepest borders / panel |
| `surface0` | `#493431` | derived lift |
| `surface1` | `#5B413D` | derived muted brown |
| `active_row_bg` | `#5B413D` | derived muted brown, focused row |
| `selection_bg` | `#A40042` | iconic magenta |
| `text` | `#E6E1C4` | fg |
| `subtext0` | `#A8977B` | derived muted label |
| `overlay1` | `#6B4E32` | comment / muted |
| `overlay0` | `#5B413D` | derived muted brown |
| `accent` | `#EFAC32` | accent gold (entity) |
| `peach` | `#EF5D32` | orange-red (keyword) |
| `yellow` | `#D9D762` | yellow (string) |
| `green` | `#7DAF9C` | sage (variable / success) |
| `red` | `#CC4232` | invalid / error |
| `teal` | `#86B4BB` | teal (xml tag) |
| `blue` | `#6C99BB` | blue (constant) |
| `mauve` | `#BE73FD` | purple (regexp) |

## The three derived values

BoP is a syntax theme. It has a background, a foreground and a set of accents, and nothing
in between — but a UI with depth needs mid-tones that a code editor never asks for.

| Hex | How |
|---|---|
| `#5B413D` | muted brown; already BoP's ANSI bright black in `terminal/`, so not new here |
| `#493431` | midpoint of `#372725` and `#5B413D`, for the shallower of the two lifts |
| `#A8977B` | midpoint of `#E6E1C4` and `#6B4E32`, a muted label that stays readable |

`#6B4E32`, the comment colour, is dim against `#372725` on purpose: right for a comment
inside a file, too dim for a sidebar label. That is what `#A8977B` is for.

`auto_switch = false`, because BoP is a dark theme with no light counterpart. herdr also
accepts `[theme.custom.light]` and `[theme.custom.dark]` if you ever want one.
