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

