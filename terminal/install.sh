#!/usr/bin/env bash
# Install the Birds Of Paradise profile into GNOME Terminal:
#   1. load the dconf dump under a fixed UUID
#   2. register the UUID in the profiles list (idempotent)
#   3. set it as the default profile
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UUID=aca24da3-722c-4f53-b35f-9832234b46f7
DCONF_PATH="/org/gnome/terminal/legacy/profiles:/:${UUID}/"

dconf load "$DCONF_PATH" < "$HERE/birds-of-paradise.dconf"
echo "loaded profile data → $DCONF_PATH"

# Register the UUID in profiles:/list if not already present.
python3 - "$UUID" <<'PYEOF'
import ast, subprocess, sys
uuid = sys.argv[1]
out = subprocess.run(
    ["dconf", "read", "/org/gnome/terminal/legacy/profiles:/list"],
    capture_output=True, text=True,
).stdout.strip()
profiles = ast.literal_eval(out) if out else []
if uuid not in profiles:
    profiles.append(uuid)
    subprocess.run(
        ["dconf", "write", "/org/gnome/terminal/legacy/profiles:/list", repr(profiles)],
        check=True,
    )
    print(f"added {uuid} to profiles list")
else:
    print(f"{uuid} already in profiles list")
PYEOF

dconf write /org/gnome/terminal/legacy/profiles:/default "'$UUID'"
echo "default profile: $(dconf read /org/gnome/terminal/legacy/profiles:/default)"
