import os
import json
import random
import re
#import googletrans
from time import sleep
from configparser import ConfigParser
import translate
from html import unescape

#translator = googletrans.Translator(service_urls=["translate.googleapis.com"])


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
        # Contains cjk?
        if not re.search(u"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]", text):
            raise ValueError("no cjk")
        #translated = translator.translate(text, "en", "ja").text
        translated = unescape(translator.translate(text))
        # Check if cp932 encodable
        translated.encode("cp932")
        return translated
    except Exception as e:
        print(e)
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


def machine_translate_list(data: dict):
    new_data = {}
    for file in data:
        new_data[file] = []
        for i, string in enumerate(data[file], start=1):
            translated = translate_text(string)
            sleep_time = random.uniform(4, 8)
            new_data[file].append(translated)
            print(f"File: {file}, Old: {repr(string)}, New: {repr(translated)}, Done {i}/{len(data[file])}, Sleeping for {round(sleep_time, 2)}s")
            sleep(sleep_time)
    return new_data


def machine_translate_single(file_name: str, data: dict):
    new_data = {}
    for i, file in enumerate(data):
        translated = translate_text(data[file])
        sleep_time = random.uniform(4, 8)
        new_data[file] = translated
        print(f"File: {file_name}, Old: {repr(data[file])}, New: {repr(translated)}, Done {i}/{len(data)}, Sleeping for {round(sleep_time, 2)}s")
        sleep(sleep_time)
    return new_data


def translate_text_files():
    # Check if already exists
    if file_exists("translated_text.json"):
        print("Skipping translated_text.json, already done.")
        return

    with open("dumped_text.json", "r", encoding="cp932") as f:
        data = json.load(f)

    new_data = machine_translate_list(data)

    with open("translated_text.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


def translate_helptext_file():
    # Check if already exists
    if file_exists("translated_helptext.json"):
        print("Skipping translated_helptext.json, already done.")
        return

    with open("dumped_helptext.json", "r", encoding="cp932") as f:
        data = json.load(f)

    new_data = machine_translate_single("HelpText.bin", data)

    with open("translated_helptext.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


def translate_tutorial_file():
    # Check if already exists
    if file_exists("translated_tutorial.json"):
        print("Skipping translated_tutorial.json, already done.")
        return

    with open("dumped_tutorial.json", "r", encoding="cp932") as f:
        data = json.load(f)

    new_data = machine_translate_single("Tutorial.bin", data)

    with open("translated_tutorial.json", "w", encoding="cp932") as f:
        json.dump(new_data, f, indent=4)


def translate_scripts():
    for root, _, files in os.walk("scripts"):
        for name in files:
            fp = os.path.join(root, name)
            config = ConfigParser()
            modified = False
            with open(fp, "r", encoding="cp932") as f:
                config.read_file(f)
                if int(config["data"]["translated"]) == 0:
                    for i, string in enumerate(config["strings"]):
                        s = config["strings"][string]
                        if s:
                            t = random.uniform(3, 7)
                            translated = translate_text(s)
                            config["strings"][string] = translated
                            print(f"File: {name}, Old: {repr(s)}, New: {repr(translated)}, Done {i}/{len(config['strings'])}, Sleeping for {round(t, 2)}s")
                            sleep(t)
                    config["data"]["translated"] = "1"
                    modified = True
            if modified:
                with open(fp, "w", encoding="cp932") as f:
                    config.write(f)


if __name__ == "__main__":
    # Machine translate dumped text/ files
    translate_text_files()

    # Machine translate dumped help/HelpText.bin file
    translate_helptext_file()

    # Machine translate dumped tutorial/Tutorial.bin file
    translate_tutorial_file()

    # Machine translate scripts
    translate_scripts()
