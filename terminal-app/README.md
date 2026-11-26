# Birds of Paradise — macOS Terminal.app profile

The same 16-colour ANSI palette and surface set as [`terminal/`](../terminal), as a
Terminal.app `.terminal` profile. Use this on a Mac; use `terminal/` on GNOME.

## Install

Double-click `birds-of-paradise.terminal`, or:

```
open birds-of-paradise.terminal
```

Terminal opens a window using the profile and adds **Birds of Paradise** to
Settings → Profiles. To keep it, select it there and click **Default**. Existing windows
keep the profile they were opened with.

macOS may warn that the file was downloaded from the internet; `xattr -d
com.apple.quarantine birds-of-paradise.terminal` clears that.

## Rebuild

```
./build.py
```

Edit `PALETTE` in `build.py`, re-run it, commit the regenerated profile. The script is pure
Python and runs anywhere — it does not need a Mac.

## File format

Terminal.app does not store colours as hex. Each one is an `NSKeyedArchiver` blob holding an
`NSColor`, base64'd into the plist, which is why this profile is generated rather than
hand-written.

**The colours are sRGB.** The lightweight archive most published `.terminal` themes use —
`NSColorSpace = 1` and an `NSRGB` string, nothing more — means *calibrated* RGB, a different
gamma, so the hex you asked for is not the hex you get. `build.py` writes an
`NSCustomColorSpace` with `NSID = 7` instead, which names sRGB. macOS 26 archives that colour
space with a 3 KB embedded ICC profile; the profile is not needed on the way back in, so the
file stays small. Verified on macOS 26.4 by unarchiving every colour in this profile through
AppKit: all 21 come back in `sRGB IEC61966-2.1` at exactly their source hex.

No `Font` key is set. A colour scheme has no business choosing a typeface, and Terminal keeps
whatever the profile it was cloned from used.

## Colour map

Identical to [`terminal/README.md`](../terminal/README.md), slot for slot.

**Surface:**

| Key | Hex | Role |
|---|---|---|
| `BackgroundColor` | `#372725` | bg |
| `TextColor` | `#E6E1C4` | fg |
| `TextBoldColor` | `#EFB732` | custom: warm gold |
| `CursorColor` | `#A40042` | custom: iconic magenta, same as selection |
| `SelectionColor` | `#A40042` | iconic magenta selection |

Terminal.app has no selection *foreground* setting; it picks one itself. The profile sets
`ShouldLimitSelectionColorToOpaqueBackground = false` so the magenta is used as given rather
than tinted toward the background.

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

## Known limit

Terminal.app has no truecolor. It renders 24-bit escape sequences by snapping them to the
nearest of these 16 colours plus the xterm-256 cube, so a program that emits exact hex — a
modern Neovim colorscheme, herdr's chrome — will not match this palette precisely. iTerm2,
Ghostty, kitty and WezTerm do not have that limit; neither does GNOME Terminal.
