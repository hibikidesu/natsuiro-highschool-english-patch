# Natsurio High School Seishun Hakusho English Translation [PS3]

# Installation
1. Unpack `npg10.cpk` from `dev_hdd0/game/BLJS10273_INSTALLDATA/USRDIR/DSC/Install` using a cpk unpacker into a folder somewhere
2. Download the `translated/` folder from [Releases](https://github.com/hibikidesu/natsuiro-highschool-english-patch/releases) or from this repo and replace the files from folder `translated/npg10/` to your unpacked directory.
4. Repack your unpacked cpk directory using CRI File System Tools with compression disabled as it seems to crash the game.
5. Send your newly packed .cpk file back where you got it from on your ps3

# For people with the 1.01 patch
The 1.01 patch causes scripts to be replaced with an updated package file making the `npg10.cpk` `script/` folder useless
1. Follow previous installation instructions
2. Unpack `npg11.cpk` from `dev_hdd0/game/BLJS10273/USRDIR/DSC/Patch` using a cpk unpacker into a folder somewhere
3. From the `translated/` folder you downloaded in the installation steps, do the same but move contents of `translated/npg11/` to your extracted `npg11.cpk` folder
4. Do steps 4 and 5 of the installation steps.

# Screenshots [WIP]
![Title Screen](https://raw.githubusercontent.com/hibikidesu/natsuiro-highschool-english-patch/master/screenshots/1.png)

# TODO
- script dump
    - script.cat 6.16%
    - script2.cat 0%
- .gtf texture modding

# File formats
## text/.bin
|        Offset        |   Size   |         Example         | Type  |                                        Notes                                         |
|----------------------|----------|-------------------------|-------|--------------------------------------------------------------------------------------|
| 0x00                 | 0x04     |             00 00 00 04 | >I    | Amount of pointers in the table                                                      |
| 0x04                 | 0x08     | 00 00 00 00 00 00 00 28 | >Q    | File offset of which location the first peice of data is located at                  |
| final pointer + 0x08 | 0x04     |             00 00 00 00 | >I    | Unknown value, unsure type (assumed is unsigned integer), may be flags or extra data |
| final pointer + 0x0C | variable |                   01 00 | char* | Could be any value, terminated with 0x00, goes on until end of file                  |
## help/HelpText.bin
Constant `0x5E` throughout the file, first part is a big endian 4 byte int (unknown usage), rest is a string terminated with `0x00`
## tutorial/Tutorial.bin
Constant `0x20` throughout the file, all are strings terminated with `0x00`
## script/LipList.bin
Unknown data. From `0x10`, size of `0x20`. First `0x10` bytes look to be a key, rest of the bytes look to be a value starting from the right position. Only ever see the last 4 bytes being used in the value.
## script/lsd.cat
Unknown.
## script/script.cat && script/script2.cat
| offset | size | notes |
|--------|------|-------|
| 0x00 | 0x04 | unknown, most are 0x0, some are 0x2000000 |
| 0x04 | 0x04 | always 00 00 00 01 |
| 0x08 | 0x08 | Main file offset, every offset is offset + main offset |
| 0x10 | 0x04 | file size - main offset |
| 0x14 | 0x08 | file count |
| 0x1c | 0x04 | always 00 00 00 00 |
| 0x20 | 0x08 | file count again? | 
| 0x28 | 0x08 | always 00 00 00 00 00 00 00 10 |
| ?    |      | |
| 0x38 | 0x04 | file offsets |
| | 0x04 | size offsets |

## present/PresentList.bin
File with a bunch of `0x01`'s `0x02`'s and `0x03`'s, unknown use.