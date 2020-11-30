from struct import unpack, pack
from functools import partial
from ctypes import create_string_buffer

__all__ = ["extract_helptext_bin", "create_helptext_bin"]


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


def create_helptext_bin(file_path: str, data: list):
    """
    Creates a helptext.bin with a given filepath

    Args:
        file_path (str): filepath to create the helptext.bin file
        data (List[int, str]): data to add to file, the list must first contain an int of a 4 byte number and string of text under 144 chars 

    Raises:
        ValueError: if str char count not under 144 characters
    """
    with open(file_path, "wb") as f:
        for item in data:
            if len(item[1]) >= 0x90:
                raise ValueError(f"'{item[1]}' exceeds character count ({len(item[1])}/143")
            f.write(pack(">I90s", item[0], item[1].encode("cp932")))
