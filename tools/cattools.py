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

        # Header
        file_size = unpack(">I", f.read(4))[0] + main_offset    # Total file size = this + specified offset
        file_count = unpack(">Q", f.read(8))[0]                 # File count
        f.read(4)                                               # Unused 4 bytes                                         
        assert unpack(">Q", f.read(8))[0] == file_count         # Should be true
        assert unpack(">Q", f.read(8))[0] == 0x10               # Always 0x10
        f.read(4)                                               # Unknown 4 bytes

        # Calc location of the file size table, not sure where 0x34 came from
        file_size = (file_count * 4) + 0x34

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


def create_cat(file_path: str, file: list):
    pass
