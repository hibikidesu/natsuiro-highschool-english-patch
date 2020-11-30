import json
import tools


def dump_helptext():
    files = tools.extract_helptext_bin("help/HelpText.bin")
    data = {}
    for file in files:
        data[file[0]] = file[1]
    with open("dumped_helptext.json", "w", encoding="cp932") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    dump_helptext()
