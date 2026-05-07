#!/usr/bin/env bash
# Install BoP-Custom GNOME Shell theme into ~/.themes/ and activate it.
# Wayland-friendly: no shell restart needed; toggling the User Themes
# extension is enough to live-reload the CSS.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/BoP-Custom"
DEST="$HOME/.themes/BoP-Custom"
EXT="user-theme@gnome-shell-extensions.gcampax.github.com"

if [ ! -d "$SRC" ]; then
  echo "BoP-Custom not found at $SRC — run ./build.py first" >&2
  exit 1
fi

mkdir -p "$HOME/.themes"
rm -rf "$DEST"
cp -r "$SRC" "$DEST"
echo "installed → $DEST"

# Both layers must be written: dconf and gsettings desync on this key in
# either direction (see the BoP repo's main README for context).
dconf write /org/gnome/shell/extensions/user-theme/name "'BoP-Custom'"
gsettings set org.gnome.shell.extensions.user-theme name 'BoP-Custom'

# Make sure the User Themes extension is enabled and reload it.
gnome-extensions enable "$EXT" 2>/dev/null || true
gnome-extensions disable "$EXT"
sleep 1
gnome-extensions enable "$EXT"

echo "active theme: $(gsettings get org.gnome.shell.extensions.user-theme name)"
