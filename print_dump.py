import json


def print_dump():
    """For testing purposes as json encodes encoding"""
    with open("dumped_text.json", "r", encoding="cp932") as f:
        data = json.load(f)
    for file in data:
        print(file)
        for string in data[file]:
            print(string)
    

if __name__ == "__main__":
    print_dump()
