#!/usr/bin/env python3
"""
bild-vorbereiten.py — bereitet ein Foto fuer emilhundt.com auf.

Nimmt ein beliebiges Foto (JPG, PNG, HEIC vom iPhone, WebP), dreht es
anhand der EXIF-Daten richtig herum, entfernt Metadaten und schreibt
WebP-Dateien in den img/-Ordner — in genau der Namens- und Groessen-
konvention, die der Rest der Seite schon benutzt:

    img/s<SLIDE>-<INDEX>-<slug>-<BREITE>.webp

Aufruf:
    python3 tools/bild-vorbereiten.py QUELLE --slide 79 --index 0 --slug "pumpkin-pie"

Gibt am Ende JSON auf stdout aus: die erzeugten Dateien mit Breite/Hoehe,
damit das srcset und width/height im HTML exakt stimmen.
"""

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "img"

# Die Seite liefert bisher immer eine 800px-Variante plus das Original
# (auf MAX_WIDTH begrenzt). Sehr kleine Bilder bekommen nur eine Datei.
SMALL_WIDTH = 800
MAX_WIDTH = 2200
QUALITY = 82


def slugify(text: str) -> str:
    """'Pâté en Croûte' -> 'p-t-en-cro-te' (gleiche Logik wie die Bestandsdateien)."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    text = re.sub(r"-{2,}", "-", text)
    return text[:32].strip("-") or "bild"


def load(src: Path):
    """Oeffnet das Bild EXIF-korrekt. HEIC laeuft ueber ImageMagick."""
    from PIL import Image, ImageOps

    if src.suffix.lower() in {".heic", ".heif"}:
        tmp = src.with_suffix(".__tmp.png")
        subprocess.run(
            ["convert", str(src), "-auto-orient", str(tmp)],
            check=True, capture_output=True,
        )
        im = Image.open(tmp).convert("RGB")
        im.load()
        tmp.unlink(missing_ok=True)
        return im

    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    if im.mode == "RGBA":
        from PIL import Image as _I
        bg = _I.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    return im


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", help="Pfad zum Originalfoto")
    p.add_argument("--slide", type=int, required=True, help="Slide-Nummer, z.B. 79")
    p.add_argument("--index", type=int, default=0, help="Position im Block (0, 1, 2 ...)")
    p.add_argument("--slug", required=True, help="Kurzname, z.B. 'Pumpkin Pie'")
    args = p.parse_args()

    src = Path(args.source).expanduser()
    if not src.is_file():
        print(json.dumps({"error": f"Datei nicht gefunden: {src}"}))
        return 1

    IMG_DIR.mkdir(exist_ok=True)
    slug = slugify(args.slug)
    im = load(src)
    native_w, native_h = im.size

    target_w = min(native_w, MAX_WIDTH)
    widths = sorted({SMALL_WIDTH, target_w}) if target_w > SMALL_WIDTH + 100 else [target_w]

    out = []
    for w in widths:
        h = round(native_h * w / native_w)
        resized = im if w == native_w else im.resize((w, h), __import__("PIL.Image", fromlist=["Image"]).LANCZOS)
        name = f"s{args.slide}-{args.index}-{slug}-{w}.webp"
        path = IMG_DIR / name
        resized.save(path, "WEBP", quality=QUALITY, method=6)
        out.append({
            "file": f"img/{name}",
            "width": w,
            "height": h,
            "kb": round(path.stat().st_size / 1024, 1),
        })

    largest = out[-1]
    srcset = ", ".join(f"{o['file']} {o['width']}w" for o in out)
    print(json.dumps({
        "ok": True,
        "source": str(src),
        "native": [native_w, native_h],
        "orientation": "hochkant" if native_h > native_w else "quer",
        "files": out,
        "src": largest["file"],
        "srcset": srcset,
        "width": largest["width"],
        "height": largest["height"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
