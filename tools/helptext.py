from struct import unpack, pack
from functools import partial
from ctypes import create_string_buffer

__all__ = ["extract_helptext_bin"]


def extract_helptext_bin(file_path: str) -> list:
    """
    Extracts help/HelpText.bin, parses it and turns it into a list.

    Args:
        file_path (str): file path pointing to help/HelpText.bin

    Returns:
        list: List of strings contained in the file + unknown number?
    """
    data = []
    with open(file_path, "rb") as f:
        # Chunk peices in 0x5E
        for chunk in iter(partial(f.read, 0x5E), b""):
            unpacked = unpack(">I90s", chunk)
            # Create string buffer and decode
            text = create_string_buffer(unpacked[1]).value.decode("cp932")
            data.append([unpacked[0], text])
    return data
