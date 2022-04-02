from typing import Dict, Optional

from sroloc.color.bank import ColorBank
from sroloc.color.utils import RgbColor, UnknownColorError, is_hex_color


class TrueColor(ColorBank[RgbColor]):
    _DEFAULT_COLOR: Optional[RgbColor] = RgbColor(255, 255, 255)
    _BANK: Dict[str, RgbColor] = dict()

    @classmethod
    def add_hex_color_to_bank(cls, name: str, color: str) -> None:
        rgb_color = RgbColor.from_hex(color)
        cls.add_color_to_bank(name, rgb_color)

    @classmethod
    def get_color(cls, name: str) -> RgbColor:
        try:
            return cls._BANK[name]
        except KeyError:
            try:
                return RgbColor.from_hex(name)
            except ValueError:
                if cls._DEFAULT_COLOR is not None:
                    return cls._DEFAULT_COLOR

                raise UnknownColorError(name)

    @classmethod
    def has_color(cls, name: str) -> bool:
        return is_hex_color(name) or super().has_color(name)

    @classmethod
    def fg_color_code(cls, color: str) -> str:
        r, g, b = cls.get_color(color)
        return f'38;2;{r};{g};{b}'

    @classmethod
    def bg_color_code(cls, color: str) -> str:
        r, g, b = cls.get_color(color)
        return f'48;2;{r};{g};{b}'
