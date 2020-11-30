import os
import json
import tools


def dump_helptext():
    files = tools.extract_helptext_bin("help/HelpText.bin")
    data = {}
    for file in files:
        data[file[0]] = file[1]
    with open("dumped_helptext.json", "w", encoding="cp932") as f:
        json.dump(data, f, indent=4)


def dump_text_bin():
    dump = {}
    # For bin text file in text folder of working directory
    for file in os.listdir("text"):
        # Dump strings from file
        dumped = tools.extract_text_bin(os.path.join("text", file))
        dump[file] = dumped
        print(f"Dumped {file}")
    with open("dumped_text.json", "w", encoding="cp932") as f:
        json.dump(dump, f, indent=4)


def dump_tutorial():
    files = tools.extract_tutorial_bin("tutorial/Tutorial.bin")
    data = {}
    for i, file in enumerate(files):
        data[i] = file
    with open("dumped_tutorial.json", "w", encoding="cp932") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    dump_helptext()
    dump_text_bin()
    dump_tutorial()