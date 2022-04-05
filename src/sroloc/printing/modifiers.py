from enum import IntEnum


class ColorModifier(IntEnum):
    reset = 0
    bold = 1
    faint = 2


class TextModifier(IntEnum):
    italic = 3
    underline = 4
    blink = 5
    blink_fast = 6
    reverse_video = 7
    erase = 8
    strikethrough = 9
