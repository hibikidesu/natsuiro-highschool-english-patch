import os
import struct
import tools
import configparser
from io import BytesIO
from ctypes import create_string_buffer


def dump_bin(data: bytes) -> configparser.ConfigParser:
    data = BytesIO(data)
    config = configparser.ConfigParser()
    
    # Read offset of bin
    data.seek(0x10)
    bin_offset = struct.unpack(">I", data.read(4))[0]
    data.seek(bin_offset)
    end_offset = struct.unpack(">I", data.read(4))[0]
    data.seek(bin_offset)
    file_count = (end_offset - bin_offset) // 4

    # Read strings
    dumped = []
    for file in range(file_count):
        offset = struct.unpack(">I", data.read(0x04))[0]
        next_offset = data.tell()
        if offset == 0x00:
            break
        data.seek(offset)
        
        # Extract string
        string = b""
        while True:
            byte = data.read(1)
            if byte == b"\x00":
                break
            string += byte
        dumped.append(string.decode("cp932"))

        # Go to next offset
        data.seek(next_offset)
    
    # Get file size
    data.seek(0, 2)
    file_size = data.tell()

    config["data"] = {
        "offset": bin_offset,
        "size": file_size - bin_offset
    }
    config["strings"] = {}

    for i, string in enumerate(dumped, start=1):
        config["strings"][f"string{i}"] = string

    data.close()
    return config


def dump_scripts(script_path: str):
    files = tools.extract_cat(script_path)
    for i, file in enumerate(files):
        with open(os.path.join("scripts", f"{i}.ini"), "w", encoding="cp932") as f:
            config = dump_bin(file)
            config.write(f)
        print(f"Extracted {i}")


if __name__ == "__main__":
    dump_scripts("script/script.cat")
