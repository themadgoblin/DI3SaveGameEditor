import sys
import zlib
import struct

# File format
# uint32 version;
# uint32 totalFilesize;
# uint32 StorageCompression;
# uint32 originalSize (uncompressed);
# uint32 unpaddedSize (from CMP1 to end of file); NEEDS TO BE PADDED
# uint32 StorageEncryption;
# string "CMP1"
# uint32 decompressedSize;
# uint32 compressedSize;
# uint32 decompressedHash;
# uint32 compressedHash;

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

def calculate_checksum(data):
    return 0x00000000

def decompress_file(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        version = struct.unpack('<I', f.read(4))[0]
        total_filesize = struct.unpack('<I', f.read(4))[0]
        storage_compression = struct.unpack('<I', f.read(4))[0]
        original_size = struct.unpack('<I', f.read(4))[0]
        unpadded_size = struct.unpack('<I', f.read(4))[0]
        storage_encryption = struct.unpack('<I', f.read(4))[0]

        print("Parsed header:")
        print(f"  Version: {version}")
        print(f"  Total Filesize: {total_filesize}")
        print(f"  Storage Compression: {bool(storage_compression)}")
        print(f"  Original Size: {original_size}")
        print(f"  Unpadded Size: {unpadded_size}")
        print(f"  Storage Encryption: {bool(storage_encryption)}")

        # Scan for CMP1 magic marker
        found_magic = False
        while True:
            byte = f.read(1)
            if not byte:
                print("Error: 'CMP1' magic string not found in file.")
                return
            if byte == b'C':
                peek = byte + f.read(3)
                if peek == b'CMP1':
                    magic = peek
                    found_magic = True
                    break
                else:
                    f.seek(-3, 1)

        if not found_magic:
            print("Error: CMP1 marker not found.")
            return

        uncompressed_size = struct.unpack('<i', f.read(4))[0]
        compressed_size = struct.unpack('<i', f.read(4))[0]
        uncompressed_checksum = struct.unpack('<I', f.read(4))[0]
        compressed_checksum = struct.unpack('<I', f.read(4))[0]
        compressed_data = f.read()

    print("CMP1 Block info:")
    print(f"  Magic: {magic.decode(errors='replace')}")
    print(f"  Uncompressed Size: {uncompressed_size}")
    print(f"  Compressed Size: {compressed_size}")
    print(f"  Uncompressed Checksum: 0x{uncompressed_checksum:08X}")
    print(f"  Compressed Checksum: 0x{compressed_checksum:08X}")

    try:
        decompressed_data = zlib.decompress(compressed_data)
        with open(output_filename, 'wb') as out:
            out.write(decompressed_data)
        print(f"Decompressed data written to: {output_filename}")
    except zlib.error as e:
        print(f"Decompression failed: {e}")

def compress_file(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        raw_data = f.read()

    compressed_data = zlib.compress(raw_data)
    uncompressed_size = len(raw_data)
    compressed_size = len(compressed_data)

    uncompressed_checksum = hash_file(raw_data, len(raw_data), 0)
    compressed_checksum = hash_file(compressed_data, len(compressed_data), 0)

    # Build CMP1 block
    cmp1_block = b''
    cmp1_block += b'CMP1'
    cmp1_block += struct.pack('<i', uncompressed_size)
    cmp1_block += struct.pack('<i', compressed_size)
    cmp1_block += struct.pack('<I', uncompressed_checksum)
    cmp1_block += struct.pack('<I', compressed_checksum)
    cmp1_block += compressed_data

    # Pad to 16-byte boundary
    pad_len = (16 - (len(cmp1_block) % 16)) % 16
    cmp1_block += b'\x00' * pad_len
    unpadded_size = len(cmp1_block)
    total_filesize = 64 + unpadded_size

    with open(output_filename, 'wb') as out:
        out.write(struct.pack('<I', 519))  # version
        out.write(struct.pack('<I', total_filesize))  # totalFilesize
        out.write(struct.pack('<I', 1))  # StorageCompression (True)
        out.write(struct.pack('<I', uncompressed_size))  # originalSize
        out.write(struct.pack('<I', unpadded_size))  # unpaddedSize
        out.write(struct.pack('<I', 0))  # StorageEncryption (False)
        out.write(b'\x00' * (64 - 24))  # pad to 64 bytes

        out.write(cmp1_block)

    print(f"Compressed data written to: {output_filename}")
    print(f"  Uncompressed Size: {uncompressed_size}")
    print(f"  Compressed Size: {compressed_size}")
    print(f"  Padding Added: {pad_len} bytes")
    print(f"  Unpadded Block Size: {unpadded_size}")
    print(f"  Total File Size: {total_filesize}")
    print(f"  Uncompressed Checksum: 0x{uncompressed_checksum:08X}")
    print(f"  Compressed Checksum: 0x{compressed_checksum:08X}")

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] not in ('-c', '-d'):
        print(f"Usage:")
        print(f"  {sys.argv[0]} -d <input_file> <output_file>    # Decompress")
        print(f"  {sys.argv[0]} -c <input_file> <output_file>    # Compress")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if mode == '-d':
        decompress_file(input_file, output_file)
    elif mode == '-c':
        compress_file(input_file, output_file)
