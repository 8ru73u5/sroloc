from abc import ABC
from typing import ClassVar, Optional, Dict

from sroloc.color.bank import ColorBank
from sroloc.color.utils import InvalidAnsiColorValueError

_ANSI_BASIC_COLORS = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'purple': 5,
    'cyan': 6,
    'white': 7
}

_ANSI_EXTENDED_COLORS = {
    'black': 0,
    'maroon': 1,
    'green': 2,
    'olive': 3,
    'navy': 4,
    'purple': 5,
    'teal': 6,
    'silver': 7,
    'grey': 8,
    'red': 9,
    'lime': 10,
    'yellow': 11,
    'blue': 12,
    'fuchsia': 13,
    'aqua': 14,
    'white': 15,
    'grey_0': 16,
    'navy_blue': 17,
    'dark_blue': 18,
    'blue_3': 19,
    'blue_3_alt': 20,
    'blue_1': 21,
    'dark_green': 22,
    'deep_sky_blue_4_alt': 23,
    'deep_sky_blue_4_alt_1': 24,
    'deep_sky_blue_4_alt_2': 25,
    'dodger_blue_3': 26,
    'dodger_blue_2': 27,
    'green_4': 28,
    'spring_green_4': 29,
    'turquoise_4': 30,
    'deep_sky_blue_3': 31,
    'deep_sky_blue_3_alt': 32,
    'dodger_blue_1': 33,
    'green_3': 34,
    'spring_green_3': 35,
    'dark_cyan': 36,
    'light_sea_green': 37,
    'deep_sky_blue_2': 38,
    'deep_sky_blue_1': 39,
    'green_3_alt': 40,
    'spring_green_3_alt': 41,
    'spring_green_2': 42,
    'cyan_3': 43,
    'dark_turquoise': 44,
    'turquoise_2': 45,
    'green_1': 46,
    'spring_green_2_alt': 47,
    'spring_green_1': 48,
    'medium_spring_green': 49,
    'cyan_2': 50,
    'cyan_1': 51,
    'dark_red': 52,
    'deep_pink_4': 53,
    'purple_4': 54,
    'purple_4_alt': 55,
    'purple_3': 56,
    'blue_violet': 57,
    'orange_4': 58,
    'grey_37': 59,
    'medium_purple_4': 60,
    'slate_blue_3': 61,
    'slate_blue_3_alt': 62,
    'royal_blue_1': 63,
    'chartreuse_4': 64,
    'dark_sea_green_4': 65,
    'pale_turquoise_4': 66,
    'steel_blue': 67,
    'steel_blue_3': 68,
    'cornflower_blue': 69,
    'chartreuse_3': 70,
    'dark_sea_green_4_alt': 71,
    'cadet_blue': 72,
    'cadet_blue_alt': 73,
    'sky_blue_3': 74,
    'steel_blue_1': 75,
    'chartreuse_3_alt': 76,
    'pale_green_3': 77,
    'sea_green_3': 78,
    'aquamarine_3': 79,
    'medium_turquoise': 80,
    'steel_blue_1_alt': 81,
    'chartreuse_2': 82,
    'sea_green_2': 83,
    'sea_green_1': 84,
    'sea_green_1_alt': 85,
    'aquamarine_1': 86,
    'dark_slate_gray_2': 87,
    'dark_red_alt': 88,
    'deep_pink_4_alt': 89,
    'dark_magenta': 90,
    'dark_magenta_alt': 91,
    'dark_violet': 92,
    'purple_alt': 93,
    'orange_4_alt': 94,
    'light_pink_4': 95,
    'plum_4': 96,
    'medium_purple_3_alt': 97,
    'medium_purple_3_alt_1': 98,
    'slate_blue_1': 99,
    'yellow_4': 100,
    'wheat_4': 101,
    'grey_53': 102,
    'light_slate_grey': 103,
    'medium_purple': 104,
    'light_slate_blue': 105,
    'yellow_4_alt': 106,
    'dark_olive_green_3': 107,
    'dark_sea_green': 108,
    'light_sky_blue_3': 109,
    'light_sky_blue_3_alt': 110,
    'sky_blue_2': 111,
    'chartreuse_2_alt': 112,
    'dark_olive_green_3_alt': 113,
    'pale_green_3_alt': 114,
    'dark_sea_green_3': 115,
    'dark_slate_gray_3': 116,
    'sky_blue_1': 117,
    'chartreuse_1': 118,
    'light_green': 119,
    'light_green_alt': 120,
    'pale_green_1': 121,
    'aquamarine_1_alt': 122,
    'dark_slate_gray_1': 123,
    'red_3': 124,
    'deep_pink_4_alt_1': 125,
    'medium_violet_red': 126,
    'magenta_3': 127,
    'dark_violet_alt': 128,
    'purple_alt_1': 129,
    'dark_orange_3': 130,
    'indian_red': 131,
    'hot_pink_3': 132,
    'medium_orchid_3': 133,
    'medium_orchid': 134,
    'medium_purple_2': 135,
    'dark_goldenrod': 136,
    'light_salmon_3': 137,
    'rosy_brown': 138,
    'grey_63': 139,
    'medium_purple_2_alt': 140,
    'medium_purple_1': 141,
    'gold_3': 142,
    'dark_khaki': 143,
    'navajo_white_3': 144,
    'grey_69': 145,
    'light_steel_blue_3': 146,
    'light_steel_blue': 147,
    'yellow_3': 148,
    'dark_olive_green_3_alt_1': 149,
    'dark_sea_green_3_alt': 150,
    'dark_sea_green_2': 151,
    'light_cyan_3': 152,
    'light_sky_blue_1': 153,
    'green_yellow': 154,
    'dark_olive_green_2': 155,
    'pale_green_1_alt': 156,
    'dark_sea_green_2_alt': 157,
    'dark_sea_green_1': 158,
    'pale_turquoise_1': 159,
    'red_3_alt': 160,
    'deep_pink_3': 161,
    'deep_pink_3_alt': 162,
    'magenta_3_alt': 163,
    'magenta_3_alt_1': 164,
    'magenta_2': 165,
    'dark_orange_3_alt': 166,
    'indian_red_alt': 167,
    'hot_pink_3_alt': 168,
    'hot_pink_2': 169,
    'orchid': 170,
    'medium_orchid_1': 171,
    'orange_3': 172,
    'light_salmon_3_alt': 173,
    'light_pink_3': 174,
    'pink_3': 175,
    'plum_3': 176,
    'violet': 177,
    'gold_3_alt': 178,
    'light_goldenrod_3': 179,
    'tan': 180,
    'misty_rose_3': 181,
    'thistle_3': 182,
    'plum_2': 183,
    'yellow_3_alt': 184,
    'khaki_3': 185,
    'light_goldenrod_2': 186,
    'light_yellow_3': 187,
    'grey_84': 188,
    'light_steel_blue_1': 189,
    'yellow_2': 190,
    'dark_olive_green_1': 191,
    'dark_olive_green_1_alt': 192,
    'dark_sea_green_1_alt': 193,
    'honeydew_2': 194,
    'light_cyan_1': 195,
    'red_1': 196,
    'deep_pink_2': 197,
    'deep_pink_1': 198,
    'deep_pink_1_alt': 199,
    'magenta_2_alt': 200,
    'magenta_1': 201,
    'orange_red_1': 202,
    'indian_red_1': 203,
    'indian_red_1_alt': 204,
    'hot_pink': 205,
    'hot_pink_alt': 206,
    'medium_orchid_1_alt': 207,
    'dark_orange': 208,
    'salmon_1': 209,
    'light_coral': 210,
    'pale_violet_red_1': 211,
    'orchid_2': 212,
    'orchid_1': 213,
    'orange_1': 214,
    'sandy_brown': 215,
    'light_salmon_1': 216,
    'light_pink_1': 217,
    'pink_1': 218,
    'plum_1': 219,
    'gold_1': 220,
    'light_goldenrod_2_alt': 221,
    'light_goldenrod_2_alt_1': 222,
    'navajo_white_1': 223,
    'misty_rose_1': 224,
    'thistle_1': 225,
    'yellow_1': 226,
    'light_goldenrod_1': 227,
    'khaki_1': 228,
    'wheat_1': 229,
    'cornsilk_1': 230,
    'grey_100': 231,
    'grey_3': 232,
    'grey_7': 233,
    'grey_11': 234,
    'grey_15': 235,
    'grey_19': 236,
    'grey_23': 237,
    'grey_27': 238,
    'grey_30': 239,
    'grey_35': 240,
    'grey_39': 241,
    'grey_42': 242,
    'grey_46': 243,
    'grey_50': 244,
    'grey_54': 245,
    'grey_58': 246,
    'grey_62': 247,
    'grey_66': 248,
    'grey_70': 249,
    'grey_74': 250,
    'grey_78': 251,
    'grey_82': 252,
    'grey_85': 253,
    'grey_89': 254,
    'grey_93': 255
}


class ANSIColor(ColorBank[int], ABC):
    _BITS_PER_COLOR: ClassVar[int]  # Should be only 3 or 8

    @classmethod
    def add_color_to_bank(cls, name: str, color: int) -> None:
        if color < 0 or color >= (2 ** cls._BITS_PER_COLOR):
            raise InvalidAnsiColorValueError(color, cls._BITS_PER_COLOR)

        super().add_color_to_bank(name, color)


class BasicColor(ANSIColor):
    _BANK: Dict[str, int] = _ANSI_BASIC_COLORS
    _DEFAULT_COLOR: Optional[int] = _BANK['white']
    _BITS_PER_COLOR = 3

    @classmethod
    def fg_color_code(cls, color: str) -> str:
        color_code = cls.get_color(color)
        return '3' + str(color_code)

    @classmethod
    def bg_color_code(cls, color: str) -> str:
        color_code = cls.get_color(color)
        return '4' + str(color_code)


class ExtendedColor(ANSIColor):
    _BANK: Dict[str, int] = _ANSI_EXTENDED_COLORS
    _DEFAULT_COLOR: Optional[int] = _BANK['white']
    _BITS_PER_COLOR = 8

    @classmethod
    def fg_color_code(cls, color: str) -> str:
        color_code = cls.get_color(color)
        return '38;5;' + str(color_code)

    @classmethod
    def bg_color_code(cls, color: str) -> str:
        color_code = cls.get_color(color)
        return '48;5;' + str(color_code)
