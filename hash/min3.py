import sys

def hash_file(k: bytes, length: int, initval: int) -> int:
    def mix(a, b, c):
        a = (a - b - c) & 0xffffffff; a ^= (c >> 13)
        b = (b - c - a) & 0xffffffff; b ^= (a << 8) & 0xffffffff
        c = (c - a - b) & 0xffffffff; c ^= (b >> 13)
        a = (a - b - c) & 0xffffffff; a ^= (c >> 12)
        b = (b - c - a) & 0xffffffff; b ^= (a << 16) & 0xffffffff
        c = (c - a - b) & 0xffffffff; c ^= (b >> 5)
        a = (a - b - c) & 0xffffffff; a ^= (c >> 3)
        b = (b - c - a) & 0xffffffff; b ^= (a << 10) & 0xffffffff
        c = (c - a - b) & 0xffffffff; c ^= (b >> 15)
        return a & 0xffffffff, b & 0xffffffff, c & 0xffffffff

    a = b = 0x9e3779b9
    c = initval
    pos = 0

    while length - pos >= 12:
        a += int.from_bytes(k[pos:pos+4], 'little')
        b += int.from_bytes(k[pos+4:pos+8], 'little')
        c += int.from_bytes(k[pos+8:pos+12], 'little')
        a, b, c = mix(a & 0xffffffff, b & 0xffffffff, c & 0xffffffff)
        pos += 12

    c += length
    remainder = k[pos:]

    if len(remainder) >= 11: c += remainder[10] << 24
    if len(remainder) >= 10: c += remainder[9] << 16
    if len(remainder) >= 9:  c += remainder[8] << 8
    if len(remainder) >= 8:  b += remainder[7] << 24
    if len(remainder) >= 7:  b += remainder[6] << 16
    if len(remainder) >= 6:  b += remainder[5] << 8
    if len(remainder) >= 5:  b += remainder[4]
    if len(remainder) >= 4:  a += remainder[3] << 24
    if len(remainder) >= 3:  a += remainder[2] << 16
    if len(remainder) >= 2:  a += remainder[1] << 8
    if len(remainder) >= 1:  a += remainder[0]

    a, b, c = mix(a & 0xffffffff, b & 0xffffffff, c & 0xffffffff)
    return c & 0xffffffff

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)

    result = hash_file(data, len(data), 0)
    print(f"Hash: 0x{result:08x}")

if __name__ == "__main__":
    main()
