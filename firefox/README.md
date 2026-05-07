# Birds of Paradise — Firefox theme

A pure-JSON Firefox `theme` extension. No SVGs, no images — Firefox theming is just a manifest with a color map.

## Install (signed, normal Firefox)

`about:addons` → ⚙ (gear) → **Install Add-on From File…** → pick `firefox-bop-1.1.0.xpi`.

The addon ID `birds-of-paradise@thomas.lacroix.e` is stable across versions, so future bumps install in-place over the existing entry.

## Build a new version

1. Bump `version` in `manifest.json`.
2. `./build.sh` → produces `firefox-bop-<version>-unsigned.xpi`.
3. Upload that to <https://addons.mozilla.org/developers/addon/submit/> under **"On your own"** (self-distribution). AMO auto-signs it.
4. Download the signed `.xpi`, drop it into this folder, commit.

## Color map (from `manifest.json`)

| Firefox slot | Hex | BoP role |
|---|---|---|
| `frame` / `frame_inactive` | `#2E211F` | one-step-darker chrome |
| `tab_selected` / `toolbar` / `ntp_background` | `#372725` | body |
| `tab_text` / `toolbar_text` / `bookmark_text` | `#E6E1C4` | foreground cream |
| `tab_line` / `toolbar_field_border_focus` / `icons_attention` / `popup_highlight` | `#EFAC32` | accent gold |
| `tab_loading` | `#EF5D32` | orange-red (keyword) |
| `toolbar_field` / `popup` / `sidebar` | `#2E211F` | popovers |
| `toolbar_field_border` / `*_separator` | `#1F1413` | deepest borders |
| `toolbar_field_highlight` | `#A40042` | iconic magenta selection |
| `toolbar_field_highlight_text` | `#FFF9D5` | warm white on magenta |
