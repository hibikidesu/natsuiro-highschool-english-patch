import json
import tools


def dump_tutorial():
    files = tools.extract_tutorial_bin("tutorial/Tutorial.bin")
    data = {}
    for i, file in enumerate(files):
        data[i] = file
    with open("dumped_tutorial.json", "w", encoding="cp932") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    dump_tutorial()
