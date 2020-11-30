import json
import os
import tools


def build_text():
    os.makedirs(os.path.join("translated", "text"), exist_ok=True)
    with open("translated_text.json", "r", encoding="cp932") as f:
        data = json.load(f)
    for file in data:
        tools.create_text_bin(os.path.join("translated", "text", file), data[file])
        print(f"Created {file}")


if __name__ == "__main__":
    build_text()
