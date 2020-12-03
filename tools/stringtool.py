import struct

__all__ = ["extract_strings", "extract_strings_s"]


def extract_strings(file_path: str, minsize: int = 1) -> dict:
    """
    Extracts all strings in a binary file

    Args:
        file_path (str): The file path to extract strings from
        minsize (int): Min len of string to search for

    Returns:
        dict: Offset of the string as a key, value will be the string contents and length.
    """
    dumped = {}

    # wow mess
    buffer = []
    offset = 0
    with open(file_path, "rb") as f:
        # Read in 128 byte chunks
        c = f.read(128)
        # While read() != 0
        while c != b"":
            # For each byte in 128 bytes
            for byte in c:
                offset += 1
                # If byte is null, append to array, clear buffer
                if byte == 0x00:
                    # If is greater than min keep size
                    if len(buffer) > minsize:
                        # Test if decodable
                        try:
                            content = bytes(buffer).decode("cp932")
                            dumped[hex(offset - len(buffer) - 1)] = {
                                "size": len(buffer),
                                "content": content
                            }
                        except:
                            pass
                    # Clear buffer
                    buffer = []
                else:
                    # Add new byte if not null byte
                    buffer.append(byte)
            # Keep reading
            c = f.read(128)

    return dumped


def extract_strings_s(file_path: str, offset: int, size: int, minsize: int = 0) -> dict:
    """
    Read string at offset for specified size

    Args:
        file_path (str): File path
        offset (int): File offset to read as
        size (int): Length to read
        minsize (int, optional): Min size of a string. Defaults to 0.

    Returns:
        dict: Offset of the string as a key, value will be the string contents and length.
    """
    buffer = []
    dumped = {}
    count = 0
    with open(file_path, "rb") as f:
        # Seek to offset
        f.seek(offset)
        c = f.read(128)
        # Read until end of file and before size
        while c != b"" and count <= size:
            # For each byte in 128 bytes
            for byte in c:
                if count >= size:
                    break
                offset += 1
                count += 1
                # If byte is null, append to array, clear buffer
                if byte == 0x00:
                    # If is greater than min keep size
                    if len(buffer) > minsize:
                        # Test if decodable
                        try:
                            content = bytes(buffer).decode("cp932")
                            dumped[hex(offset - len(buffer) - 1)] = {
                                "size": len(buffer),
                                "content": content
                            }
                        except:
                            pass
                    # Clear buffer
                    buffer = []
                else:
                    # Add new byte if not null byte
                    buffer.append(byte)
            c = f.read(128)
    return dumped
