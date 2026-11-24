#!/usr/bin/env python3
"""Generate birds-of-paradise.terminal, a macOS Terminal.app profile.

Terminal.app stores each colour as an NSKeyedArchiver blob rather than as a hex string, so
the profile cannot be written by hand the way the GNOME Terminal dconf dump can. This script
builds those blobs directly; it is pure Python and needs no Mac to run.

**The colours are sRGB, exactly.** The lightweight archive every community .terminal file
uses (`NSColorSpace = 1`, an `NSRGB` string, nothing else) means *calibrated* RGB, which
macOS renders with a different gamma, so `#372725` arrives on screen as something else.
Emitting `NSCustomColorSpace` with `NSID = 7` instead names sRGB. macOS 26 archives that
colour space with a 3 KB embedded ICC profile; the profile is not needed on the way back in.
Verified on macOS 26.4 by unarchiving this script's output through AppKit:

    space: sRGB IEC61966-2.1
    srgb: 0.215686 0.152941 0.145098   # #372725, unchanged

Run `./build.py` after editing PALETTE, then commit the regenerated profile.
"""

from __future__ import annotations

import plistlib
from pathlib import Path
from plistlib import UID

OUT = Path(__file__).resolve().parent / "birds-of-paradise.terminal"

PROFILE_NAME = "Birds of Paradise"

# Same 16 ANSI slots and surface colours as terminal/birds-of-paradise.dconf, so a GNOME
# Terminal and a Terminal.app window show the same thing. Roles are the tmTheme's.
PALETTE = {
    # surface
    "BackgroundColor": "#372725",  # bg
    "TextColor": "#E6E1C4",  # fg
    "TextBoldColor": "#E6E1C4",  # fg; BoP has no separate bold colour
    "CursorColor": "#DDDDDD",  # cursor body
    "SelectionColor": "#A40042",  # iconic magenta
    # normal
    "ANSIBlackColor": "#1F1413",  # deepest border
    "ANSIRedColor": "#CC4232",  # invalid
    "ANSIGreenColor": "#7DAF9C",  # sage / variable
    "ANSIYellowColor": "#EFAC32",  # accent gold
    "ANSIBlueColor": "#6C99BB",  # constant
    "ANSIMagentaColor": "#BE73FD",  # regexp special
    "ANSICyanColor": "#86B4BB",  # xml tag
    "ANSIWhiteColor": "#E6E1C4",  # foreground cream
    # bright
    "ANSIBrightBlackColor": "#5B413D",  # muted brown
    "ANSIBrightRedColor": "#EF5D32",  # keyword orange-red
    "ANSIBrightGreenColor": "#9CCEBA",  # sage light
    "ANSIBrightYellowColor": "#D9D762",  # string
    "ANSIBrightBlueColor": "#AFC4DB",  # preprocessor
    "ANSIBrightMagentaColor": "#C699BB",  # sass values
    "ANSIBrightCyanColor": "#A6D4DC",  # teal light
    "ANSIBrightWhiteColor": "#F8F8F8",  # bright
}


def archived_color(hex_color: str) -> bytes:
    """One NSColor in sRGB, as Terminal.app expects to find it in the profile."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    components = f"{r:.8f} {g:.8f} {b:.8f} 1".encode()
    objects = [
        "$null",
        {
            "$class": UID(3),
            # Read only when NSCustomColorSpace is missing. Kept because that is the shape
            # AppKit writes, and an unarchiver that ignores the custom space still gets a
            # colour rather than nothing.
            "NSColorSpace": 1,
            "NSComponents": components,
            "NSCustomColorSpace": UID(2),
            "NSRGB": components,
        },
        {"$class": UID(4), "NSID": 7},  # 7 = sRGB
        {"$classes": ["NSColor", "NSObject"], "$classname": "NSColor"},
        {"$classes": ["NSColorSpace", "NSObject"], "$classname": "NSColorSpace"},
    ]
    return plistlib.dumps(
        {
            "$archiver": "NSKeyedArchiver",
            "$objects": objects,
            "$top": {"root": UID(1)},
            "$version": 100000,
        },
        fmt=plistlib.FMT_BINARY,
    )


def build() -> dict:
    profile = {
        "name": PROFILE_NAME,
        # Terminal.app will not import a plist that does not say what kind of settings it is.
        "type": "Window Settings",
        # The schema version Terminal has written since 10.9. Omitting it also imports, but
        # Terminal then rewrites the profile on first use, which makes the next diff noise.
        "ProfileCurrentVersion": 2.04,
        # Selection uses the magenta as given rather than tinting it toward the background.
        "ShouldLimitSelectionColorToOpaqueBackground": False,
        # No Font key on purpose: a colour scheme has no business picking a typeface.
    }
    for key, value in PALETTE.items():
        profile[key] = archived_color(value)
    return profile


def main() -> None:
    OUT.write_bytes(plistlib.dumps(build(), fmt=plistlib.FMT_XML))
    print(f"wrote {OUT} ({len(PALETTE)} colours)")


if __name__ == "__main__":
    main()
