# Natsurio High School Seishun Hakusho English Translation [PS3]

# Installation
1. Unpack npg10.cpk from `dev_hdd0/game/BLJS10273_INSTALLDATA/USRDIR/DSC/Install` using a cpk unpacker into
2. Download the `translated/` folder from [Releases](http://example.com) and replace files to your unpacked directory
3. Repack your unpacked cpk directory using CRI File System Tools with compression disabled as it seems to crash the game.
4. Send your newly packed .cpk file back where you got it from on your ps3

# TODO
- .cat file format dumping
- .gtf texture modding

# File formats
## .bin
|        Offset        |   Size   |         Example         | Type  |                                        Notes                                         |
|----------------------|----------|-------------------------|-------|--------------------------------------------------------------------------------------|
| 0x00                 | 0x04     |             00 00 00 04 | >I    | Amount of pointers in the table                                                      |
| 0x04                 | 0x08     | 00 00 00 00 00 00 00 28 | >Q    | File offset of which location the first piece of data is located at                  |
| final pointer + 0x08 | 0x04     |             00 00 00 00 | >I    | Unknown value, unsure type (assumed is unsigned integer), may be flags or extra data |
| final pointer + 0x0C | variable |                   01 00 | char* | Could be any value, terminated with 0x00, goes on until end of file                  |
