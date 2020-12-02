import json
import os
import tools


def build_text():
    os.makedirs(os.path.join("translated", "npg10", "text"), exist_ok=True)
    with open("translated_text.json", "r", encoding="cp932") as f:
        data = json.load(f)
    for file in data:
        tools.create_text_bin(os.path.join("translated", "npg10", "text", file), data[file])
        print(f"Created text/{file}")


def build_helptext():
    os.makedirs(os.path.join("translated", "npg10", "help"), exist_ok=True)
    with open("translated_helptext.json", "r", encoding="cp932") as f:
        data = json.load(f)
    out = []
    for x in data:
        out.append([int(x), data[x]])
    tools.create_helptext_bin(os.path.join("translated", "npg10", "help", "HelpText.bin"), out)
    print("Created help/HelpText.bin")


def build_tutorial():
    os.makedirs(os.path.join("translated", "npg10", "tutorial"), exist_ok=True)
    with open("translated_tutorial.json", "r", encoding="cp932") as f:
        data = json.load(f)
    out = []
    for x in data:
        out.append(data[x])
    tools.create_tutorial_bin(os.path.join("translated", "npg10", "tutorial", "Tutorial.bin"), out)
    print("Created tutorial/Tutorial.bin")


if __name__ == "__main__":
    build_text()
    build_helptext()
    build_tutorial()
