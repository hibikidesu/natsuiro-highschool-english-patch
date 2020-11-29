import os
import json
import random
import googletrans
from time import sleep

translator = googletrans.Translator()


def translate_text(text: str):
    try:
        translated = translator.translate(text, "en", "ja").text
        # Check if cp932 encodable
        translated.encode("cp932")
        return translated
    except:
        print(f"Failed to translate {text}")
        return text


def translate_text_files():
    with open("dumped_text.json", "r", encoding="cp932") as f:
        data = json.load(f)
    new_data = {}
    for file in data:
        new_data[file] = []
        for i, string in enumerate(data[file], start=1):
            translated = translate_text(string)
            sleep_time = random.uniform(4, 8)
            new_data[file].append(translated)
            print(f"File: {file}, Old: {string}, New: {translated}, Done {i}/{len(data[file])}, Sleeping for {round(sleep_time, 2)}s")
            sleep(sleep_time)

    with open("translated_text.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


if __name__ == "__main__":
    # Machine translate dumped text/ files
    os.makedirs(os.path.join("translated", "text"), exist_ok=True)
    translate_text_files()
