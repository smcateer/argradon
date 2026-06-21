from __future__ import annotations

import io
import re
import sys
import zipfile
from pathlib import Path

import requests
from fontTools.ttLib import TTFont

FAMILY = "Mournmore Code"
OUT = Path("dist")

UPSTREAM_REPO = "githubnext/monaspace"
RELEASES_API = f"https://api.github.com/repos/{UPSTREAM_REPO}/releases/latest"

# Mournmore mapping:
# Regular      = Argon Frozen Regular
# Italic       = Radon Frozen Regular
# Bold         = Argon Frozen Bold
# Bold Italic  = Radon Frozen Bold
WANTED = [
    ("MonaspaceArgonFrozen-Regular.ttf", "Regular", "MournmoreCode-Regular"),
    ("MonaspaceRadonFrozen-Regular.ttf", "Italic", "MournmoreCode-Italic"),
    ("MonaspaceArgonFrozen-Bold.ttf", "Bold", "MournmoreCode-Bold"),
    ("MonaspaceRadonFrozen-Bold.ttf", "Bold Italic", "MournmoreCode-BoldItalic"),
]


def latest_release_zip_url() -> str:
    response = requests.get(RELEASES_API, timeout=30)
    response.raise_for_status()
    release = response.json()

    # Prefer source zipball. This is stable enough for now.
    return release["zipball_url"]


def download_zip(url: str) -> zipfile.ZipFile:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return zipfile.ZipFile(io.BytesIO(response.content))


def find_file(zf: zipfile.ZipFile, filename: str) -> bytes:
    matches = [name for name in zf.namelist() if name.endswith(filename)]
    if not matches:
        raise FileNotFoundError(f"Could not find {filename} in upstream release zip")

    # If several match, prefer ttf/static/frozen-ish paths.
    matches.sort(key=lambda p: ("frozen" not in p.lower(), "ttf" not in p.lower(), len(p)))
    return zf.read(matches[0])


def set_name(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]

    # Update existing records.
    for record in name_table.names:
        if record.nameID == name_id:
            record.string = value.encode(record.getEncoding(), errors="replace")

    # Add common Windows/Unicode record if missing.
    if not any(r.nameID == name_id for r in name_table.names):
        name_table.setName(value, name_id, 3, 1, 0x409)


def rename_font(font_bytes: bytes, style: str, ps_name: str) -> TTFont:
    font = TTFont(io.BytesIO(font_bytes))

    full_name = f"{FAMILY} {style}"

    # Name table
    set_name(font, 1, FAMILY)       # Font Family
    set_name(font, 2, style)        # Font Subfamily
    set_name(font, 4, full_name)    # Full name
    set_name(font, 6, ps_name)      # PostScript name
    set_name(font, 16, FAMILY)      # Typographic family
    set_name(font, 17, style)       # Typographic subfamily

    # OS/2 fsSelection bits help Windows style-linking.
    if "OS/2" in font:
        os2 = font["OS/2"]

        # Clear italic/bold/regular bits: bit 0 italic, bit 5 bold, bit 6 regular.
        os2.fsSelection &= ~(1 << 0)
        os2.fsSelection &= ~(1 << 5)
        os2.fsSelection &= ~(1 << 6)

        if "Italic" in style:
            os2.fsSelection |= 1 << 0
        if "Bold" in style:
            os2.fsSelection |= 1 << 5
        if style == "Regular":
            os2.fsSelection |= 1 << 6

        # Weight class
        os2.usWeightClass = 700 if "Bold" in style else 400

    # head.macStyle bits: bit 0 bold, bit 1 italic.
    if "head" in font:
        head = font["head"]
        head.macStyle &= ~0b11
        if "Bold" in style:
            head.macStyle |= 0b01
        if "Italic" in style:
            head.macStyle |= 0b10

    return font


def main() -> int:
    OUT.mkdir(exist_ok=True)

    zf = download_zip(latest_release_zip_url())

    for upstream_filename, style, ps_name in WANTED:
        print(f"Building {ps_name}.ttf from {upstream_filename}")
        source_bytes = find_file(zf, upstream_filename)
        font = rename_font(source_bytes, style, ps_name)
        font.save(OUT / f"{ps_name}.ttf")

    print("Built:")
    for path in sorted(OUT.glob("*.ttf")):
        print(f"  {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
