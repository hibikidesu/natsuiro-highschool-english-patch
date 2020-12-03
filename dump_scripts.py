import os
import tools
import configparser


# Name, Offset, Size
# npg11.cpk -> script/script.cat
offsets = [
    ["prologue", 0x4e30, 0x21c],
    ["ev002", 0x5780, 0x29f],
    ["ev003", 0x6150, 0x219],
    ["ev004", 0x7b20, 0x17a5],
    ["ev005", 0x99f0, 0x2ce],
    ["ev005", 0x9f69, 0xdd],
    ["ev005", 0xa2a0, 0xbc],
    ["ev005", 0xb460, 0x680],
    ["megu_heroine_birthday", 0xd7a0, 0x1b9f],
    ["prologue_2", 0x11550, 0x14cd],
    ["chr001_mail0050", 0x13930, 3160],
    ["unknown", 0x15250, 2335],
    ["megu", 0x16970, 2730],
    ["megu_date", 0x17670, 74],
    ["megu_date", 0x187c0, 3239],
    ["unknown", 0x19ea0, 2434],
    ["unknown", 0x1b120, 1573],
    ["unknown", 0x1bf40, 1486],
    ["megu_date", 0x1ca80, 906],
    ["megu_date", 0x1d2f0, 885],
    ["megu", 0x1e290, 2553],
    ["unknown", 0x1f4a0, 1832],
    ["unknown", 0x2049d, 1999],
    ["megu_school_festival_maze_1_s", 0x21110, 455],
    ["megu_school_festival_maze_1_l", 0x21650, 758],
    ["megu_school_festival_maze_1_l", 0x21d60, 814],
    ["megu_school_festival_maze_1_l", 0x22590, 1208],
    ["megu_school_festival_maze_1_l", 0x22e70, 705],
    ["school_festival_bloomers_cafe_2", 0x24a22, 6110],
    ["megu_school_festival_fortune_telling_3", 0x27740, 4743],
    ["ev007", 0x29af0, 5603],
    ["ev007", 0x2be70, 4628],
    ["megu", 0x2d740, 1108],
    ["megu_camp_3_liver_test_2", 0x2e160, 786],
    ["megu_camp_3_liver_test_3", 0x2ea10, 1093],
    ["megu_camp_3_liver_test_4", 0x2f400, 1195],
    ["megu_camp_3_liver_test_5", 0x30710, 2324],
    ["ev001", 0x34100, 8898],
    ["ev002", 0x39f44, 12318],
    ["ev003", 0x40340, 8613],
    ["ev004", 0x45800, 7624],
    ["ev005", 0x49770, 5652],
    ["ev006", 0x4d094, 4881],
    ["ev007", 0x50b80, 6435],
    ["ev008", 0x55794, 9911],
    ["ev009", 0x5b3f0, 8497],
    ["ev010", 0x61480, 9304],
    ["ev011", 0x65c50, 6046],
    ["ev012", 0x6a990, 8280]
]


def dump_scripts(script_path: str):
    for i, offset in enumerate(offsets):
        # Extract strings from file at offset and for size
        strings = tools.extract_strings_s(script_path, offset[1], offset[2])

        # Create new config
        config = configparser.ConfigParser()
        # Write strings to config
        for line in strings:
            config[line] = strings[line]
        
        with open(os.path.join("scripts", f"{i}_{offset[0]}.txt"), "w", encoding="cp932") as f:
            config.write(f)


if __name__ == "__main__":
    dump_scripts("script/script.cat")
