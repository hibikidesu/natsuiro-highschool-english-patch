from struct import unpack, pack

__all__ = ["extract_text_bin", "create_text_bin"]


def extract_text_bin(file_path: str) -> list:
    """
    Extracts a data from a .bin file

    Args:
        file_path (str): file path of the .bin file

    Returns:
        list: list of each file data
    """
    # List of data values
    data = []
    pointers = []
    flags = 0

    with open(file_path, "rb") as f:
        # Get the amount of pointers in the table
        pointer_count = unpack(">I", f.read(4))[0]

        # Get file offsets for each pointer in the table
        for _ in range(pointer_count):
            pointers.append(unpack(">Q", f.read(8))[0])

        # Extra flags? unused? table seperator?
        flags = unpack(">I", f.read(4))[0]

        # Read data from pointers
        for pointer in pointers:
            # Seek to pointer position
            f.seek(pointer)
            
            # Read string until hit null
            string = b""
            while True:
                byte = f.read(1)
                if byte == b"\x00":
                    break
                string += byte
            data.append(string.decode("cp932"))

    return data


def create_text_bin(file_path: str, data: list):
    """
    Repack all data 1:1 as to what it should be

    Args:
        file_path (str): File path of the .bin file to be made
        data (list): list of data that should be packed into the file
    """
    with open(file_path, "wb") as f:
        # Write file pointer count
        f.write(pack(">I", len(data)))

        # Calculate the first position where data will start at
        data_start_position = 0x04 + (0x08 * len(data)) + 0x04

        # Write pointers to table
        for text in data:
            text = text.encode("cp932")
            f.write(pack(">Q", data_start_position))
            data_start_position += (len(text) + 1)

        # ?
        f.write(pack(">I", 0))

        # Write data
        for text in data:
            text = text.encode("cp932") + b"\x00"
            f.write(text)
