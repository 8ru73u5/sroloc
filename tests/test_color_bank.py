import pytest

from sroloc.color.ansi import BasicColor, ExtendedColor
from sroloc.color.true import TrueColor
from sroloc.color.utils import RgbColor, UnknownColorError, \
    InvalidAnsiColorValueError


@pytest.fixture(scope='function')
def true_color_empty():
    prev_bank = TrueColor._BANK
    prev_default_color = TrueColor._DEFAULT_COLOR

    TrueColor._BANK = dict()
    TrueColor._DEFAULT_COLOR = None
    yield TrueColor

    TrueColor._BANK = prev_bank
    TrueColor._DEFAULT_COLOR = prev_default_color


@pytest.fixture(scope='function')
def basic_color_empty():
    prev_bank = BasicColor._BANK
    prev_default_color = BasicColor._DEFAULT_COLOR

    BasicColor._BANK = dict()
    BasicColor._DEFAULT_COLOR = None
    yield BasicColor

    BasicColor._BANK = prev_bank
    BasicColor._DEFAULT_COLOR = prev_default_color


def test_add_true_color_to_bank(true_color_empty):
    color_name = 'black'
    color_value = RgbColor(0, 0, 0)
    true_color_empty.add_color_to_bank(color_name, color_value)

    assert true_color_empty._BANK[color_name] == color_value


def test_add_hex_true_color_to_bank(true_color_empty):
    color_name = 'black'
    color_hex_value = '#000000'
    color_rgb_value = RgbColor(0, 0, 0)

    true_color_empty.add_hex_color_to_bank(color_name, color_hex_value)

    assert true_color_empty._BANK[color_name] == color_rgb_value


def test_add_two_identically_named_true_colors_to_bank(true_color_empty):
    color_name = 'black'
    color_value1 = RgbColor(0, 0, 0)
    color_value2 = RgbColor(1, 1, 1)

    true_color_empty.add_color_to_bank(color_name, color_value1)
    true_color_empty.add_color_to_bank(color_name, color_value2)

    assert true_color_empty._BANK[color_name] == color_value2


def test_get_known_true_color(true_color_empty):
    color_name = 'black'
    color_value = RgbColor(0, 0, 0)

    true_color_empty._BANK = {color_name: color_value}

    assert true_color_empty._BANK[color_name] == color_value


def test_get_unknown_true_color_with_default_color(true_color_empty):
    default_color = RgbColor(0, 0, 0)
    true_color_empty._DEFAULT_COLOR = default_color

    assert true_color_empty.get_color('invalid_name') == default_color


def test_get_unknown_true_color_without_default_color(true_color_empty):
    with pytest.raises(UnknownColorError):
        true_color_empty.get_color('invalid_name')


def test_get_hex_true_color_without_default_color(true_color_empty):
    color_name = '#000000'
    color_value = RgbColor(0, 0, 0)

    assert true_color_empty.get_color(color_name) == color_value


def test_add_ansi_color_to_bank(basic_color_empty):
    color_name = 'black'
    color_value = 0

    basic_color_empty.add_color_to_bank(color_name, color_value)

    assert basic_color_empty._BANK[color_name] == color_value


@pytest.mark.parametrize('ansi_version,color_value', [
    (BasicColor, -1),
    (BasicColor, 8),
    (ExtendedColor, -1),
    (ExtendedColor, 256)
])
def test_add_invalid_ansi_color_to_bank(ansi_version, color_value):
    with pytest.raises(InvalidAnsiColorValueError):
        ansi_version.add_color_to_bank('invalid_color', color_value)


def test_get_known_ansi_color(basic_color_empty):
    color_name = 'black'
    color_value = 0

    basic_color_empty._BANK = {color_name: color_value}

    assert basic_color_empty.get_color(color_name) == color_value


def test_get_unknown_ansi_color_with_default_color(basic_color_empty):
    default_color = 0
    basic_color_empty._DEFAULT_COLOR = default_color

    assert basic_color_empty.get_color('invalid_color') == default_color


def test_get_unknown_ansi_color_without_default_color(basic_color_empty):
    with pytest.raises(UnknownColorError):
        basic_color_empty.get_color('invalid_color')


def test_has_color(basic_color_empty):
    color_name = 'black'
    basic_color_empty._BANK = {color_name: 0}

    assert basic_color_empty.has_color(color_name) is True
    assert basic_color_empty.has_color('invalid_color') is False


def test_has_true_color(true_color_empty):
    color_name = 'black'
    true_color_empty._BANK = {color_name: RgbColor(0, 0, 0)}

    assert true_color_empty.has_color(color_name) is True
    assert true_color_empty.has_color('invalid_color') is False
    assert true_color_empty.has_color('#00ff00') is True


def test_set_default_color_value(basic_color_empty):
    default_color = 0
    basic_color_empty.set_default_color(default_color)

    assert basic_color_empty._DEFAULT_COLOR == default_color


def test_set_default_color_from_bank(basic_color_empty):
    default_color_name = 'black'
    default_color_value = 0

    basic_color_empty._BANK = {default_color_name: default_color_value}
    basic_color_empty.set_default_color_from_bank(default_color_name)

    assert basic_color_empty._DEFAULT_COLOR == default_color_value
