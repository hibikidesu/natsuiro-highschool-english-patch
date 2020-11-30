import os
import json
import random
import googletrans
from time import sleep

translator = googletrans.Translator()


def translate_text(text: str):
    """
    Translates jp text into en text and returns it as a string

    Args:
        text (str): jp text to translate

    Returns:
        [type]: en translated text

    Raises:
        Exception: if failed to encode or translate text
    """
    try:
        translated = translator.translate(text, "en", "ja").text
        # Check if cp932 encodable
        translated.encode("cp932")
        return translated
    except:
        print(f"Failed to translate {text}")
        return text


def file_exists(file: str) -> bool:
    """
    Checks if file exists

    Args:
        file (str): location of file to check in current directory

    Returns:
        [bool]: if exists
    """
    return os.path.isfile(file)


def translate_text_files():
    # Check if already exists
    if file_exists("translated_text.json"):
        print("Skipping translated_text.json, already done.")
        return

    with open("dumped_text.json", "r", encoding="cp932") as f:
        data = json.load(f)

    new_data = {}
    for file in data:
        new_data[file] = []
        for i, string in enumerate(data[file], start=1):
            translated = translate_text(string)
            sleep_time = random.uniform(4, 8)
            new_data[file].append(translated)
            print(f"File: {file}, Old: {repr(string)}, New: {repr(translated)}, Done {i}/{len(data[file])}, Sleeping for {round(sleep_time, 2)}s")
            sleep(sleep_time)

    with open("translated_text.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


def translate_helptext_file():
    # Check if already exists
    if file_exists("translated_helptext.json"):
        print("Skipping translated_helptext.json, already done.")
        return

    with open("dumped_helptext.json", "r", encoding="cp932") as f:
        data = json.load(f)

    new_data = {}
    for i, file in enumerate(data):
        translated = translate_text(data[file])
        sleep_time = random.uniform(4, 8)
        new_data[file] = translated
        print(f"File: HelpText.bin, Old: {repr(data[file])}, New: {repr(translated)}, Done {i}/{len(data)}, Sleeping for {round(sleep_time, 2)}s")
        sleep(sleep_time)

    with open("translated_helptext.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


if __name__ == "__main__":
    # Machine translate dumped text/ files
    translate_text_files()

    # Machine translate dumped help/HelpText.bin file
    translate_helptext_file()
