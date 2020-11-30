import os
import json
import tools


def dump_bin():
    dump = {}
    # For bin text file in text folder of working directory
    for file in os.listdir("text"):
        # Dump strings from file
        dumped = tools.extract_text_bin(os.path.join("text", file))
        dump[file] = dumped
        print(f"Dumped {file}")
    with open("dumped_text.json", "w", encoding="cp932") as f:
        json.dump(dump, f, indent=4)


if __name__ == "__main__":
    dump_bin()
