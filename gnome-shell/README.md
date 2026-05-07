# BoP-Custom — GNOME Shell theme

A recolored Yaru-dark for GNOME 46, replacing every cool gray and Ubuntu accent with Birds of Paradise warm browns, ambers, and creams. **Shape and geometry are stock Yaru-dark** — only colors are changed. This is intentional: previous attempts (`Gruvbox-Orange-Dark-Medium`, `BoP-Yellow-Dark-Medium`) altered top-bar/dock geometry and broke layout.

## Install

```
./install.sh
```

This copies `BoP-Custom/` into `~/.themes/` and activates it via dconf + gsettings + the User Themes extension. Wayland-friendly (no shell restart needed; the extension toggle reloads in-place).

## Rebuild from upstream Yaru-dark

`build.py` regenerates `BoP-Custom/` from a Yaru-dark source. Use this when Ubuntu ships a Yaru-dark update and you want to pull in the new geometry while keeping BoP colors.

```
./build.py                                                       # default source: /usr/share/themes/Yaru-dark/gnome-shell
./build.py --source /path/to/another/Yaru-dark/gnome-shell       # custom source
```

`cp -rL` is mandatory because Ubuntu's `/usr/share/themes/Yaru-dark/gnome-shell` is a symlink to `/usr/share/gnome-shell/theme/Yaru-dark/`. The script handles this for you.

## What the build does

1. Copies the Yaru-dark shell theme directory (dereferencing the symlink).
2. Substitutes colors in `gnome-shell.css`:
   - **Pure-gray hex** (`#XXXXXX` where R=G=B) → BoP browns, bucketed by luminance.
   - **Pure-gray rgba** (`rgba(R,G,B,a)` where R=G=B) → matching BoP rgba, alpha preserved.
   - **Off-white rgba** (`rgba(238,238,236,…)`, `rgba(255,255,255,…)`) → cream `rgba(230,225,196,…)`.
   - **Yaru orange variants** → BoP ambers (`#EFAC32`, `#F1B64A`, `#C5850F`, `#DD9511`).
   - **Yaru reds** → BoP error `#CC4232`.
   - **Yaru greens** → BoP sage `#7DAF9C`.
   - **`#FFFFFF`** → BoP warm white `#FFF9D5`.
3. Appends a small override block: gives inactive Quick Settings pills a tinted bg `#3F2826` (with hover `#4B3331`) — without this, inactive pills inherit only a faint cream-on-brown overlay and read as cool/neutral against the active amber pills.

The luminance buckets for grays:

| Yaru luminance | BoP brown |
|---|---|
| `<0x20` | `#1F1413` |
| `<0x40` | `#2E211F` |
| `<0x60` | `#5C4F44` |
| `<0x80` | `#6B4E32` |
| `<0xA0` | `#806A4A` |
| `<0xC0` | `#A8997D` |
| `≥0xC0` | `#E6E1C4` (cream) |
