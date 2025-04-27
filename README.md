# DI3SaveGameEditor
## May the 4th be with you.

Packer and unpacker for Disney Infinity save game files. 
Original hashing function by Bob Jenkins, Dec 1996. Code can be found on the hash directory.

You can find your savegame files here:
```
C:\Users\[WindowsUserName]\AppData\Roaming\Disney Interactive\Disney Infinity 1.0\[ID]\SavedGame\win32
C:\Users\[WindowsUserName]\AppData\Roaming\Disney Interactive\Disney Infinity 3.0\[ID]\SavedGame\user0
```


## Usage

Requires Python 3

### Decompress a file

```
inflate.py -d <input_file> <output_file>

```

### Compress a file

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



## Supported versions

| Platform   | Version   | Status   |
|------------|-----------|----------|
| PC         | 1.0       | Works    |
| PC         | 2.0       | Untested |
| PC         | 3.0       | Untested |


## Supported files

Savegames on PC use a naming convention:

[Type of save][World][Save number]

### Types (incomplete)

```
[E] Contains the HelpManager. Its purpose is unknown.
[EH] Contains the CSaveGameSlot. Metadata about the save file.
[S] The savegame data. Level structure, unlocks, etc...
[SC] Thumbnail of the level.
[P0] Special file. Only one for each player. Seems to contain global data.
```

### Worlds (incomplete)

```
[EM] Empire Strikes Back
[IO] Inside Out
[PZ] PSZ
[PX] PSX
[BA] Marvel Battle Arena
[MO] Moana
[RO] TBX_Onboard
[CW] The Clone Wars
[RT] Takeover
[RR] Rumpus Room , AKA Toybox mode
[RI] Rumpus Room , Interior

```

