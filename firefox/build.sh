#!/usr/bin/env bash
# Pack manifest.json into an unsigned .xpi ready for AMO self-distribution upload.
# AMO will return a signed .xpi which is what you actually install.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

VERSION=$(python3 -c 'import json,sys; print(json.load(open("manifest.json"))["version"])')
OUT="firefox-bop-${VERSION}-unsigned.xpi"

rm -f "$OUT"
zip -j -q "$OUT" manifest.json

echo "wrote $OUT"
echo "upload at https://addons.mozilla.org/developers/addon/submit/ ('On your own')"
echo "then drop the signed xpi back into this folder and commit it."
