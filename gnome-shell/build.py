#!/usr/bin/env python3
"""Rebuild BoP-Custom GNOME Shell theme from a Yaru-dark source.

Copies the Yaru-dark shell theme (dereferencing the symlink that
/usr/share/themes/Yaru-dark/gnome-shell points into the gnome-shell pkg)
and applies a deterministic color substitution to gnome-shell.css.
Shape, sizing, and assets are unchanged — only colors are remapped.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path


def gray_to_bop(v: int) -> tuple[int, int, int]:
    """Bucket a pure-gray luminance into a BoP brown by tier."""
    if v < 0x20: return (0x1F, 0x14, 0x13)
    if v < 0x40: return (0x2E, 0x21, 0x1F)
    if v < 0x60: return (0x5C, 0x4F, 0x44)
    if v < 0x80: return (0x6B, 0x4E, 0x32)
    if v < 0xA0: return (0x80, 0x6A, 0x4A)
    if v < 0xC0: return (0xA8, 0x99, 0x7D)
    return (0xE6, 0xE1, 0xC4)


YARU_ORANGE_MAP = {
    "#EF845F": "#F1B64A", "#F4A88D": "#F2BD5D",
    "#FAB248": "#F1B64A", "#FAAE3E": "#F1B64A", "#FAA52A": "#EFAC32",
    "#E84F19": "#EFAC32", "#EC6B3E": "#F1B64A", "#EB6030": "#EFAC32",
    "#EA5D2C": "#EFAC32", "#E95C2A": "#EFAC32", "#E95420": "#EFAC32",
    "#E64C17": "#C5850F", "#E54C17": "#C5850F", "#C54113": "#C5850F",
    "#D34615": "#C5850F", "#EF8661": "#F1B64A", "#F99B11": "#DD9511",
    "#8D2F0E": "#8D6504", "#481807": "#4B330B",
}

YARU_RED_MAP = {
    "#DE1930": "#CC4232", "#C7162B": "#CC4232",
    "#E82D43": "#CC4232", "#E7243B": "#CC4232",
    "#A71224": "#991121",
}

YARU_GREEN_MAP = {
    "#0C6D1A": "#5A8275", "#073F0F": "#3D5A4F",
    "#33BE49": "#7DAF9C", "#339A3B": "#7DAF9C",
    "#2FAE43": "#7DAF9C", "#2EAA42": "#7DAF9C",
    "#2B9E3D": "#7DAF9C", "#2A9A3B": "#7DAF9C",
    "#258A35": "#7DAF9C", "#217A2F": "#5A8275",
}


QUICK_TOGGLE_OVERRIDE = """

/* BoP-Custom override: warm-tinted Quick Settings inactive pills + arrows.
   Lower CSS specificity than .quick-toggle:checked, so active amber pills
   are unaffected. Without this, inactive pills inherit only a faint
   cream-on-brown overlay and read as cool against the active amber. */
.quick-toggle,
.quick-menu-toggle .quick-toggle,
.quick-menu-toggle .quick-toggle-arrow {
  background-color: #3F2826;
}
.quick-toggle:hover,
.quick-menu-toggle .quick-toggle:hover,
.quick-menu-toggle .quick-toggle-arrow:hover {
  background-color: #4B3331;
}
"""


DOCK_COMPACT_OVERRIDE = """

/* BoP-Custom override: very compact bottom dock chrome.
   Ubuntu Dock's stylesheet
   (/usr/share/gnome-shell/extensions/ubuntu-dock@ubuntu.com/stylesheet.css)
   adds 24 logical px of vertical padding around each dock icon
   (padding-top: 10px + padding-bottom: 14px), plus a 4px margin under
   the dash background and another 14px padding-top in fixed mode.
   We zero those out so the dock sits flush against the icons.
   !important is required: the extension stylesheet loads after the
   shell theme and matches/exceeds our selector specificity. */
#dashtodockContainer.bottom #dash .dash-item-container .app-well-app,
#dashtodockContainer.bottom #dash .dash-item-container .show-apps,
#dashtodockContainer.bottom #dash .dash-item-container .overview-tile {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}
#dashtodockContainer.bottom #dash .dash-background {
  margin-bottom: 0 !important;
}
#dashtodockContainer.bottom.fixed #dash .dash-item-container .app-well-app,
#dashtodockContainer.bottom.fixed #dash .dash-item-container .show-apps {
  padding-top: 0 !important;
}
#dashtodockContainer.bottom.fixed #dash .dash-background {
  margin-top: 0 !important;
}
"""


def transform_css(text: str) -> str:
    # Pure-gray hex (R==G==B), 6-digit
    def hex6_repl(m: re.Match) -> str:
        s = m.group(0)
        r, g, b = int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16)
        if r == g == b:
            nr, ng, nb = gray_to_bop(r)
            return f"#{nr:02X}{ng:02X}{nb:02X}"
        return s

    text = re.sub(r"#[a-fA-F0-9]{6}", hex6_repl, text)

    # Pure-gray rgba(R, G, B, a)
    def rgba_gray_repl(m: re.Match) -> str:
        r, g, b, a = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        if r == g == b:
            nr, ng, nb = gray_to_bop(r)
            return f"rgba({nr}, {ng}, {nb},{a})"
        return m.group(0)

    text = re.sub(r"rgba\((\d+),\s*(\d+),\s*(\d+),([^)]+)\)", rgba_gray_repl, text)

    # Off-white rgba → cream rgba
    text = re.sub(r"rgba\(238,\s*238,\s*236,", "rgba(230, 225, 196,", text)
    text = re.sub(r"rgba\(255,\s*255,\s*255,", "rgba(230, 225, 196,", text)

    # Yaru orange/red/green hex variants
    for old, new in {**YARU_ORANGE_MAP, **YARU_RED_MAP, **YARU_GREEN_MAP}.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)

    # rgba forms of the most-used Yaru oranges
    text = text.replace("rgba(211, 70, 21,", "rgba(197, 133, 15,")    # #d34615 → #C5850F
    text = text.replace("rgba(239, 188, 170,", "rgba(241, 182, 74,")  # #efbcaa → #F1B64A
    text = text.replace("rgba(233, 163, 138,", "rgba(239, 172, 50,")  # → BoP gold rgba

    # Pure white
    text = re.sub(r"#FFFFFF", "#FFF9D5", text, flags=re.IGNORECASE)

    return text + QUICK_TOGGLE_OVERRIDE + DOCK_COMPACT_OVERRIDE


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", default="/usr/share/themes/Yaru-dark/gnome-shell",
                   help="Yaru-dark gnome-shell directory (default: %(default)s)")
    p.add_argument("--out", default=None,
                   help="Output theme directory (default: ./BoP-Custom/gnome-shell next to this script)")
    args = p.parse_args()

    src = Path(args.source).resolve()
    if not src.is_dir():
        print(f"source not found or not a directory: {src}", file=sys.stderr)
        return 1

    here = Path(__file__).resolve().parent
    dst = Path(args.out).resolve() if args.out else here / "BoP-Custom" / "gnome-shell"

    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, symlinks=False)  # symlinks=False follows them

    css = dst / "gnome-shell.css"
    css.write_text(transform_css(css.read_text()))

    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
