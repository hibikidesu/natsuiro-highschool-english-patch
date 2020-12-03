import json
import os
import configparser
import tools
from struct import pack
from shutil import copyfile


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


def build_scripts():
    os.makedirs(os.path.join("translated", "npg11", "script"), exist_ok=True)
    new_cat = os.path.join("translated", "npg11", "script", "script.cat")
    copyfile(os.path.join("script", "script.cat"), new_cat)
    for file in os.listdir("scripts"):
        config = configparser.ConfigParser()
        with open(os.path.join("scripts", file), "r", encoding="cp932") as f:
            config.read_file(f)
        # Patch cat
        with open(new_cat, "r+b") as f:
            for patch in list(config):
                if patch.startswith("0x"):
                    # Check if patch under limit
                    size = config[patch]["size"]
                    content = config[patch]["content"]
                    if len(content) >= int(size):
                        print(f"{file} @ {patch} oversize {len(content)}/{size}")
                    else:
                        f.seek(int(patch, 16))
                        f.write(pack(f">{size}s", content.encode("cp932")))


if __name__ == "__main__":
    build_text()
    build_helptext()
    build_tutorial()
    build_scripts()
