"""Makes the BOUNCraft logo and puts the panel's copy into BOUNCraft.jsx.

    python3 tools/logo.py --fonts FONT_DIR --version 2.0            # writes images/logo-*.png
    python3 tools/logo.py --fonts FONT_DIR --version 2.0 --embed    # ...and embeds it in BOUNCraft.jsx

The fonts aren't in this repository (Eurostile is a commercial font). FONT_DIR must hold:

    Eurostile MN Extended Bold.ttf   "BOUNC"   (Eurostile MN, Bold, extended)
    eurostile.TTF                    "raft"    (Eurostile, Regular)
    JetBrainsMono[wght].ttf          version   (JetBrains Mono, OFL, fonts.google.com/specimen/JetBrains+Mono)

Needs Pillow (pip install pillow).
"""
import argparse
import os
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORANGE = (255, 168, 40, 255)
S = 4          # drawn at 4x, then scaled down
SLANT = 0.22   # italic shear of "BOUNCraft"


def mono(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def logo(fonts, version):
    """BOUNC + raft, slanted, with the version in orange and a soft glow. None: no version."""
    big = ImageFont.truetype(os.path.join(fonts, "Eurostile MN Extended Bold.ttf"), 52 * S)
    small = ImageFont.truetype(os.path.join(fonts, "eurostile.TTF"), 50 * S)
    ver = mono(os.path.join(fonts, "JetBrainsMono[wght].ttf"), 24 * S, 800)
    pad = 16 * S
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    b1 = d.textbbox((0, 0), "BOUNC", font=big)
    b2 = d.textbbox((0, 0), "raft", font=small)
    b3 = d.textbbox((0, 0), version or "", font=ver)
    w = b1[2] - b1[0] + b2[2] - b2[0] + b3[2] - b3[0] + pad * 3
    h = b1[3] - b1[1] + pad * 3
    layer = Image.new("RGBA", (int(w * 1.3), h), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    asc_b, _ = big.getmetrics()
    asc_s, _ = small.getmetrics()
    y0 = pad - b1[1]
    x = pad
    g.text((x - b1[0], y0), "BOUNC", font=big, fill="white")
    x += b1[2] - b1[0] + 3 * S
    g.text((x - b2[0], y0 + asc_b - asc_s), "raft", font=small, fill="white")
    lw, lh = layer.size
    extra = int(lh * SLANT)
    layer = layer.transform((lw + extra, lh), Image.AFFINE, (1, SLANT, -extra, 0, 1, 0), Image.BICUBIC)
    layer = layer.crop(layer.getbbox())
    if version:
        vw = b3[2] - b3[0]
        with_ver = Image.new("RGBA", (layer.width + vw + 5 * S, layer.height), (0, 0, 0, 0))
        with_ver.alpha_composite(layer)
        ImageDraw.Draw(with_ver).text((layer.width + 4 * S - b3[0], -b3[1]), version, font=ver, fill=ORANGE)
        layer = with_ver.crop(with_ver.getbbox())
    out = Image.new("RGBA", (layer.width + 2 * pad, layer.height + 2 * pad), (0, 0, 0, 0))
    alpha = layer.split()[3].point(lambda v: int(v * 0.35))
    glow = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    glow.putalpha(alpha)
    glow_pad = Image.new("RGBA", out.size, (0, 0, 0, 0))
    glow_pad.alpha_composite(glow, (pad, pad))
    out.alpha_composite(glow_pad.filter(ImageFilter.GaussianBlur(9 * S)))
    out.alpha_composite(layer, (pad, pad))
    return out


def scaled(img, width):
    return img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)


def embed(png_path, jsx_path):
    """Replaces the bytes of `var LOGO_PNG = ...;` in the script with the PNG's."""
    data = open(png_path, "rb").read()
    lines = ['        "' + "".join("\\x%02x" % c for c in data[i:i + 29]) + '"' for i in range(0, len(data), 29)]
    value = "\n" + " +\n".join(lines) + ";"
    src = open(jsx_path, encoding="utf-8").read()
    new, n = re.subn(r'(    var LOGO_PNG =)[\s\S]*?";', lambda m: m.group(1) + value, src, count=1)
    if n != 1:
        raise SystemExit("var LOGO_PNG not found in " + jsx_path)
    open(jsx_path, "w", encoding="utf-8").write(new)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fonts", required=True, help="folder with the three fonts")
    ap.add_argument("--version", required=True, help='the version shown in the panel, e.g. "2.0"')
    ap.add_argument("--embed", action="store_true", help="put the panel logo into BOUNCraft.jsx")
    a = ap.parse_args()

    images = os.path.join(ROOT, "images")
    panel = scaled(logo(a.fonts, a.version), 360)   # the panel shows it at 180 px wide (2x)
    panel_path = os.path.join(images, "logo-panel.png")
    panel.save(panel_path, optimize=True)
    scaled(logo(a.fonts, None), 900).save(os.path.join(images, "logo.png"), optimize=True)
    print("wrote images/logo-panel.png", panel.size, "and images/logo.png")
    if a.embed:
        embed(panel_path, os.path.join(ROOT, "BOUNCraft.jsx"))
        print("embedded in BOUNCraft.jsx; check that VERSION in the script says", a.version)


if __name__ == "__main__":
    main()
