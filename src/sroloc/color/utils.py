import re
from typing import Generator


class UnknownColorError(ValueError):
    def __init__(self, color_name: str) -> None:
        self.color_name = color_name
        super().__init__(f'Color {color_name!r} is not in the color bank')


class InvalidAnsiColorValueError(ValueError):
    def __init__(self, value: int, bits_per_color: int) -> None:
        self.value = value
        self.bits_per_color = bits_per_color
        super().__init__(
            f'Invalid ANSI color value: {value}. '
            f'Should be a {bits_per_color}-bit number'
        )


class RgbToHexConversionError(ValueError):
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f'Could not convert hex to RGB: {value!r}')


_HEX_COLOR_REGEX = re.compile(
    '#[0-9a-f]{3}(([0-9a-f]{3})|([0-9a-f]{5}))?', re.I
)


def is_hex_color(hex_color: str) -> bool:
    return _HEX_COLOR_REGEX.fullmatch(hex_color.strip()) is not None


class RgbColor:
    def __init__(self, r: int, g: int, b: int, /) -> None:
        self.r, self.g, self.b = r, g, b

        if not self._validate():
            raise ValueError(f'Invalid RGB color: {self!r}')

    def _validate(self) -> bool:
        return all(
            255 >= x >= 0
            for x in self
        )

    @staticmethod
    def from_hex(hex_color: str) -> 'RgbColor':
        hex_color = hex_color.strip()

        if not is_hex_color(hex_color):
            raise RgbToHexConversionError(hex_color)

        # Remove prefix
        hex_color = hex_color[1:]

        # Remove alpha
        if len(hex_color) == 8:
            hex_color = hex_color[:6]

        # Convert shorthand form to full form
        if len(hex_color) == 3:
            hex_color = hex_color[0] * 2 + hex_color[1] * 2 + hex_color[2] * 2

        color_value = int(hex_color, 16)

        r = (color_value >> 16) & 0xff
        g = (color_value >> 8) & 0xff
        b = color_value & 0xff

        return RgbColor(r, g, b)

    def as_hex(self) -> str:
        hex_value = ''.join(f'{i:02x}' for i in self)
        return '#' + hex_value

    def __eq__(self, other) -> bool:
        if not isinstance(other, RgbColor):
            raise NotImplementedError()

        return tuple(self) == tuple(other)

    def __iter__(self) -> Generator[int, None, None]:
        yield self.r
        yield self.g
        yield self.b

    def __str__(self) -> str:
        return str(tuple(self))

    def __repr__(self) -> str:
        r, g, b = self
        return f'({r=}, {g=}, {b=})'

    def __format__(self, format_spec: str) -> str:
        if format_spec in ['h', 'hex']:
            return self.as_hex()

        if not format_spec:
            return str(self)

        raise ValueError(
            f'Invalid format specifier: {format_spec!r}'
        )
