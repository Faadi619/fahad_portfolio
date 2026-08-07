#!/usr/bin/env python3
"""Generate the tab icon from the portrait source.

Crops to the face, masks it into a circle, and composites onto the
site's deep-green field — a full headshot is unreadable at 32px, and
the transparent cutout would fray against a browser's tab background.

Called by build-images.sh; run directly to regenerate after swapping
the portrait.  Pure stdlib (zlib + struct), no dependencies.
"""

import math
import struct
import subprocess
import sys
import zlib

SRC = "Fahad Image.png"
OUT_DIR = "assets/img"
FIELD = (0x0E, 0x3D, 0x2C)          # deep green, matches the hero disc
CROP = (300, 300, 60, 70)           # w, h, x-offset, y-offset — centres the face
SIZES = {32: "favicon-32.png", 180: "apple-touch-icon.png"}


def read_png(path):
    """Decode an 8-bit PNG to (width, height, RGBA bytearray)."""
    data = open(path, "rb").read()
    pos, width, height, idat = 8, None, None, b""
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color, _, _, _ = struct.unpack(">IIBBBBB", chunk)
            if depth != 8:
                sys.exit(f"{path}: expected 8-bit, got {depth}-bit")
        elif kind == b"IDAT":
            idat += chunk
        pos += 12 + length

    raw = zlib.decompress(idat)
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    stride = width * channels
    out = bytearray(width * height * 4)
    prev = bytearray(stride)
    i = 0

    for y in range(height):
        filt = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        # Undo the per-scanline filter.
        for x in range(stride):
            a = line[x - channels] if x >= channels else 0
            b = prev[x]
            c = prev[x - channels] if x >= channels else 0
            if filt == 1:
                line[x] = (line[x] + a) & 255
            elif filt == 2:
                line[x] = (line[x] + b) & 255
            elif filt == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif filt == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if (pa <= pb and pa <= pc) else b if pb <= pc else c)) & 255
        for x in range(width):
            px = line[x * channels:(x + 1) * channels]
            if channels == 4:
                r, g, b, al = px
            elif channels == 3:
                r, g, b = px
                al = 255
            elif channels == 2:
                r = g = b = px[0]
                al = px[1]
            else:
                r = g = b = px[0]
                al = 255
            o = (y * width + x) * 4
            out[o:o + 4] = bytes((r, g, b, al))
        prev = line
    return width, height, out


def write_png(path, size, pixels):
    raw = b"".join(b"\x00" + bytes(pixels[(y * size) * 4:(y * size + size) * 4])
                   for y in range(size))

    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n"
                           + chunk(b"IHDR", header)
                           + chunk(b"IDAT", zlib.compress(raw, 9))
                           + chunk(b"IEND", b""))


def main():
    w, h, x, y = CROP
    # stdout/stderr rather than capture_output: this runs under the
    # system python3, which may be 3.6.
    subprocess.run(["sips", "-c", str(w), str(h), "--cropOffset", str(x), str(y),
                    SRC, "--out", "/tmp/_favicon_face.png"],
                   check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sw, sh, src = read_png("/tmp/_favicon_face.png")

    for size, name in SIZES.items():
        out = bytearray(size * size * 4)
        centre = (size - 1) / 2
        radius = size / 2
        for py in range(size):
            for px in range(size):
                dist = math.hypot(px - centre, py - centre)
                edge = max(0.0, min(1.0, (radius - dist) + 0.5))  # antialiased rim
                if edge <= 0:
                    continue
                sx = min(sw - 1, int(px * sw / size))
                sy = min(sh - 1, int(py * sh / size))
                o = (sy * sw + sx) * 4
                alpha = src[o + 3] / 255.0
                rgb = tuple(int(src[o + i] * alpha + FIELD[i] * (1 - alpha)) for i in range(3))
                q = (py * size + px) * 4
                out[q:q + 4] = bytes(rgb + (int(255 * edge),))
        write_png(f"{OUT_DIR}/{name}", size, out)
        print(f"  {name:<22} {size}x{size}")


if __name__ == "__main__":
    main()
