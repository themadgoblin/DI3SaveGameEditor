import struct
import numpy as np
from PIL import Image

def _decode_block(data, offset):
    # Read colour0, colour1, and 32-bit lookup
    c0, c1, bits = struct.unpack_from('<HHI', data, offset)

    # Decode 565 → (r,g,b) in Python ints
    def expand565(c):
        r = ((c >> 11) & 0x1F) * 255 // 31
        g = ((c >>  5) & 0x3F) * 255 // 63
        b = ( c        & 0x1F) * 255 // 31
        return (r, g, b)

    rgb0 = expand565(c0)
    rgb1 = expand565(c1)

    # Build 4-entry palette (all opaque)
    palette = [None]*4
    palette[0] = rgb0
    palette[1] = rgb1
    if c0 > c1:
        # 4-colour mode
        palette[2] = (
            (2*rgb0[0] + rgb1[0]) // 3,
            (2*rgb0[1] + rgb1[1]) // 3,
            (2*rgb0[2] + rgb1[2]) // 3,
        )
        palette[3] = (
            (rgb0[0] + 2*rgb1[0]) // 3,
            (rgb0[1] + 2*rgb1[1]) // 3,
            (rgb0[2] + 2*rgb1[2]) // 3,
        )
    else:
        # 3-colour mode: average + duplicate the last entry
        palette[2] = (
            (rgb0[0] + rgb1[0]) // 2,
            (rgb0[1] + rgb1[1]) // 2,
            (rgb0[2] + rgb1[2]) // 2,
        )
        # instead of transparent black, repeat entry 2
        palette[3] = palette[2]

    # Unpack 16 2-bit indices → 4×4×3 uint8 block
    block = np.empty((4, 4, 3), dtype=np.uint8)
    for i in range(16):
        idx = (bits >> (2*i)) & 0x03
        y, x = divmod(i, 4)
        block[y, x] = palette[idx]

    return block

def decompress_dxt1(raw_data: bytes, width: int, height: int) -> Image.Image:
    expected_blocks = ((width+3)//4) * ((height+3)//4)
    if len(raw_data) < expected_blocks * 8:
        raise ValueError(f"Data too short: need {expected_blocks*8} bytes, got {len(raw_data)}")

    w_blocks = (width + 3) // 4
    h_blocks = (height + 3) // 4

    # Prepare empty RGB image array
    img = np.empty((height, width, 3), dtype=np.uint8)

    offset = 0
    for by in range(h_blocks):
        for bx in range(w_blocks):
            block = _decode_block(raw_data, offset)
            offset += 8

            y0, x0 = by*4, bx*4
            y1, x1 = min(y0+4, height), min(x0+4, width)

            img[y0:y1, x0:x1] = block[:y1-y0, :x1-x0]

    return Image.fromarray(img, 'RGB')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print("Usage: python decompress_dxt1.py <input.raw> <width> <height> <output.png>")
        sys.exit(1)

    in_path, w, h, out_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    with open(in_path, 'rb') as f:
        data = f.read()

    img = decompress_dxt1(data, w, h)
    img.save(out_path)
    print(f"Decompressed to {out_path}")
