from struct import pack, unpack
from functools import partial
from ctypes import create_string_buffer

__all__ = ["extract_tutorial_bin", "create_tutorial_bin"]


def extract_tutorial_bin(file_path: str) -> list:
    """
    Extracts data from tutorial/Tutorial.bin

    Args:
        file_path (str): file path pointing to tutorial.bin

    Returns:
        list: tutorial.bin contents
    """
    data = []
    with open(file_path, "rb") as f:
        # Chunk peices in 0x20
        for chunk in iter(partial(f.read, 0x20), b""):
            unpacked = unpack(">32s", chunk)
            # Create string buffer and decode
            text = create_string_buffer(unpacked[0]).value.decode("cp932")
            data.append(text)
    return data


def create_tutorial_bin(file_path: str, data: list):
    """
    Creates a tutorial.bin file

    Args:
        file_path (str): path to create tutorial.bin
        data (list): List of strings to be added to the file

    Raises:
        ValueError: if str char count not under 32 characters
    """
    with open(file_path, "wb") as f:
        for item in data:
            if len(item) >= 0x20:
                raise ValueError(f"'{item}' exceeds character count ({len(item)}/32")
            f.write(pack(">32s", item.encode("cp932")))
