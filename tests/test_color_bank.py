import pytest

from sroloc.color.ansi import BasicColor, ExtendedColor
from sroloc.color.true import TrueColor
from sroloc.color.utils import RgbColor, UnknownColorError, \
    InvalidAnsiColorValueError


def test_add_true_color_to_bank():
    TrueColor._BANK = dict()

    color_name = 'black'
    color_value = RgbColor(0, 0, 0)
    TrueColor.add_color_to_bank(color_name, color_value)

    assert TrueColor._BANK[color_name] == color_value


def test_add_hex_true_color_to_bank():
    TrueColor._BANK = dict()

    color_name = 'black'
    color_hex_value = '#000000'
    color_rgb_value = RgbColor(0, 0, 0)

    TrueColor.add_hex_color_to_bank(color_name, color_hex_value)

    assert TrueColor._BANK[color_name] == color_rgb_value


def test_add_two_identically_named_true_colors_to_bank():
    TrueColor._BANK = dict()

    color_name = 'black'
    color_value1 = RgbColor(0, 0, 0)
    color_value2 = RgbColor(1, 1, 1)

    TrueColor.add_color_to_bank(color_name, color_value1)
    TrueColor.add_color_to_bank(color_name, color_value2)

    assert TrueColor._BANK[color_name] == color_value2


def test_get_known_true_color():
    color_name = 'black'
    color_value = RgbColor(0, 0, 0)

    TrueColor._BANK = {color_name: color_value}
    TrueColor._DEFAULT_COLOR = None

    assert TrueColor._BANK[color_name] == color_value


def test_get_unknown_true_color_with_default_color():
    TrueColor._BANK = dict()

    default_color = RgbColor(0, 0, 0)
    TrueColor._DEFAULT_COLOR = default_color

    assert TrueColor.get_color('invalid_name') == default_color


def test_get_unknown_true_color_without_default_color():
    TrueColor._BANK = dict()
    TrueColor._DEFAULT_COLOR = None

    with pytest.raises(UnknownColorError):
        TrueColor.get_color('invalid_name')


def test_get_hex_true_color_without_default_color():
    TrueColor._BANK = dict()
    TrueColor._DEFAULT_COLOR = None

    color_name = '#000000'
    color_value = RgbColor(0, 0, 0)

    assert TrueColor.get_color(color_name) == color_value


def test_add_ansi_color_to_bank():
    BasicColor._BANK = dict()

    color_name = 'black'
    color_value = 0

    BasicColor.add_color_to_bank(color_name, color_value)

    assert BasicColor._BANK[color_name] == color_value


@pytest.mark.parametrize('ansi_version,color_value', [
    (BasicColor, -1),
    (BasicColor, 8),
    (ExtendedColor, -1),
    (ExtendedColor, 256)
])
def test_add_invalid_ansi_color_to_bank(ansi_version, color_value):
    ansi_version._BANK = dict()

    with pytest.raises(InvalidAnsiColorValueError):
        ansi_version.add_color_to_bank('invalid_color', color_value)


def test_get_known_ansi_color():
    color_name = 'black'
    color_value = 0

    BasicColor._BANK = {color_name: color_value}
    BasicColor._DEFAULT_COLOR = None

    assert BasicColor.get_color(color_name) == color_value


def test_get_unknown_ansi_color_with_default_color():
    BasicColor._BANK = dict()

    default_color = 0
    BasicColor._DEFAULT_COLOR = default_color

    assert BasicColor.get_color('invalid_color') == default_color


def test_get_unknown_ansi_color_without_default_color():
    BasicColor._BANK = dict()
    BasicColor._DEFAULT_COLOR = None

    with pytest.raises(UnknownColorError):
        BasicColor.get_color('invalid_color')


def test_has_color():
    BasicColor._BANK = {'black': 0}

    assert BasicColor.has_color('black') is True
    assert BasicColor.has_color('invalid_color') is False


def test_set_default_color_value():
    BasicColor._DEFAULT_COLOR = None

    default_color = 0
    BasicColor.set_default_color(default_color)

    assert BasicColor._DEFAULT_COLOR == default_color


def test_set_default_color_from_bank():
    default_color_name = 'black'
    default_color_value = 0

    BasicColor._BANK = {default_color_name: default_color_value}
    BasicColor._DEFAULT_COLOR = None

    BasicColor.set_default_color_from_bank(default_color_name)

    assert BasicColor._DEFAULT_COLOR == default_color_value
