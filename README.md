# DI3SaveGameEditor
## May the 4th be with you.

Packer and unpacker for Disney Infinity save game files. 
Original hashing function by Bob Jenkins, Dec 1996. Code can be found on the hash directory.

You can find your savegame files for PC here:
```
C:\Users\[WindowsUserName]\AppData\Roaming\Disney Interactive\Disney Infinity 1.0\[ID]\SavedGame\win32
C:\Users\[WindowsUserName]\AppData\Roaming\Disney Interactive\Disney Infinity 3.0\[ID]\SavedGame\user0
```

For other platforms (like Wii U) you will need a modded console with a save manager to extract the raw save file.
*NOTE: Please look online for information on how to do so, this is not the scope of this project.*

## Requirements

* Python version 3.8 or newer
* Access to save raw save file if playing other versions other than PC. See above section.

## Usage
```
usage: inflate.py [-h] (-c | --compress | --no-compress | -d | --decompress | --no-decompress)
                  [-e {big,little}]
                  input_file output_file

Compress or decompress DI save files

positional arguments:
  input_file            Path to input file
  output_file           Path to output file

options:
  -h, --help            show this help message and exit
  -c, --compress, --no-compress
                        Compress input file
  -d, --decompress, --no-decompress
                        Decompress input file
  -e {big,little}, --endian {big,little}
                        Endianness for header fields (default: big)
```

Set the endianness according to the platform the save file is from:
* Wii U uses big-endian.
* PC uses little-endian.

### Decompress a File
```
inflate.py -d <input_file> <output_file>

```

### Compress a File
```
inflate.py -c <input_file> <output_file>
```

### Extract the screenshot of the savegame file and convert it to PNG

```

$ python3 inflate.py -d SCCA0 SCCA0.dec
Parsed header:
  Version: 519
  Total Filesize: 51968
  Storage Compression: True
  Original Size: 108295
  Unpadded Size: 51904
  Storage Encryption: False
CMP1 Block info:
  Magic: CMP1
  Uncompressed Size: 108295
  Compressed Size: 51855
  Uncompressed Checksum: 0xFC8C1BF2
  Compressed Checksum: 0x8EFAF63C
Decompressed data written to: SCCA0.dec

$ python3 DecodedScreenshotFileToBin.py SCCA0.dec
Wrote 50880 bytes to SCCA0.bin
SCREENSHOT_WIDTH  = 424
SCREENSHOT_HEIGHT = 240

$ python3 binToPng.py SCCA0.bin 424 240 SCCA0.png
Decompressed to SCCA0.png

```


## Supported DI Games

| Platform   | DI Game   | Status   |
|------------|-----------|----------|
| PC         | 1.0       | Works    |
| PC         | 2.0       | Untested |
| PC         | 3.0       | Untested |
| Wii U      | 2.0       | Works    |


## Save Files Explanation

Savegames use a naming convention:

[Type of save][World][Save number]

### Types (Incomplete)

```
[E] Contains the HelpManager. Its purpose is unknown.
[EH] Contains the CSaveGameSlot. Metadata about the save file.
[S] The savegame data. Level structure, unlocks, etc...
[SC] Thumbnail of the level.
[P0] Special file. Only one for each player. Contains global data.
```

### Worlds (Incomplete)
* [PZ] PSZ
* [PX] PSX
* [RO] TBX_Onboard
* [RT] Takeover
* [RR] Rumpus Room , AKA Toybox mode
* [RI] Rumpus Room , Interior
* [MO] Moana - Didn't release.

#### Disney Infinity 2.0 Playset Worlds
* [AV] Avengers
* [SP] Spider-Man
* [GG] Guardians of the Galaxy

#### Disney Infinity 3.0 Playset Worlds (Incomplete)
* [EM] Rise Against the Empire
* [IO] Inside Out
* [BA] Marvel Battle Arena
* [CW] The Clone Wars
