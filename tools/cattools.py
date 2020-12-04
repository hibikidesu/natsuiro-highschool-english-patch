from struct import pack, unpack

__all__ = ["extract_cat", "create_cat"]


def extract_cat(file_path: str) -> list:
    """
    Extracts files from a .cat archive

    Args:
        file_path (str): File path to cat file

    Returns:
        list: List of file data extracted from cat
    """
    dumped = []
    with open(file_path, "rb") as f:
        # Read +offset
        f.seek(0x08)
        main_offset = unpack(">Q", f.read(8))[0]

        # Header start
        file_size = unpack(">I", f.read(4))[0] + main_offset    # Total file size = this + specified offset
        file_count = unpack(">Q", f.read(8))[0]                 # File count
        f.read(4)                                               # Unused 4 bytes                                         
        assert unpack(">Q", f.read(8))[0] == file_count         # Should be true
        assert unpack(">Q", f.read(8))[0] == 0x10               # Always 0x10
        f.read(4)                                               # Unknown 4 bytes

        # Calc location of the file size table, 0x34 -> header size
        file_size = (file_count * 4) + 0x34

        # Header end
        # We are now at 0x34 of the file, offset location
        # Iter over file count
        for file in range(file_count):
            # This is the offset of the file
            offset = unpack(">I", f.read(4))[0] + main_offset
            # This is the next offset for the next loop
            next_offset = f.tell()

            # Get the file size of this file from the table
            f.seek(file_size)
            size = unpack(">I", f.read(4))[0]
            # Set next offset in table for next loop
            file_size = f.tell()

            # Seek to the file
            f.seek(offset)

            # Read contents of size to list
            dumped.append(f.read(size))

            # Go back to the offset table to prepare for next read
            f.seek(next_offset)

    return dumped


def pad_offset(offset: int) -> int:
    """
    Calculates amount of 00's to create to pad with

    Args:
        offset (int): Offset num

    Returns:
        int: amount of 00s to be padded
    """
    n = offset % 0x10
    if n == 0:
        return 0
    return 0x10 - n


def create_cat(file_path: str, files: list):
    """
    Create 1:1 cat file from input files to output directory

    Args:
        file_path (str): File path to create cat at
        files (list): List of files to insert into archive (list of bytes only)
    """
    with open(file_path, "wb") as f:
        # Header start
        f.write(pack(">Q", 0x01))           # Write magic (assumed)
        f.write(pack(">Q", 0x20))           # Write main offset
        f.write(pack(">I", 0x00))           # File size, placeholder, REWRITE WHEN COMPLETE FILE
        f.write(pack(">Q", len(files)))     # File count #1
        f.write(pack(">I", 0x00))           # Unknown
        f.write(pack(">Q", len(files)))     # File count #2
        f.write(pack(">Q", 0x10))           # Always 0x10
        f.write(pack(">I", 0x00))           # Unknown

        # Header end
        # File offset table begin
        # Calculate the first position where data will start at
        # header size + table size + pad needed?
        data_start_position = (0x04 * len(files)) * 2
        data_start_position += pad_offset(data_start_position) + 0x10

        for file in files:
            f.write(pack(">I", data_start_position))
            data_start_position += len(file)
            data_start_position += pad_offset(data_start_position)

        # File offset table end
        # Size offset table start
        for file in files:
            f.write(pack(">I", len(file)))

        # Pad
        count = pad_offset(f.tell())
        f.write(pack(f">{count}s", b""))

        # Size offset table end
        # Write files start
        for file in files:
            # Write file
            f.write(file)
            # Pad end of file
            count = pad_offset(f.tell())
            f.write(pack(f">{count}s", b""))

        # Write files end
        # Write file size to header
        f.seek(0, 2)
        file_size = f.tell()                    # File size of the entire file
        f.seek(0x10)                            # Seek to header file offset
        f.write(pack(">I", file_size - 0x20))   # Write file size - main offset
