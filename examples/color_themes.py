from sroloc.color.true import TrueColor
from sroloc.color.utils import RgbColor

MONOKAI_COLORS = {
    'black': RgbColor(39, 40, 34),
    'red': RgbColor(249, 38, 114),
    'green': RgbColor(166, 226, 46),
    'yellow': RgbColor(230, 219, 116),
    'blue': RgbColor(102, 217, 239),
    'purple': RgbColor(253, 95, 240),
    'cyan': RgbColor(161, 239, 228),
    'white': RgbColor(248, 248, 242),
}


class MonokaiTheme(TrueColor):
    _BANK = MONOKAI_COLORS
    _DEFAULT_COLOR = _BANK['white']
