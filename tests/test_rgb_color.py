import pytest

from sroloc.color.utils import RgbColor, RgbToHexConversionError


def test_create_valid_rgb_color():
    r, g, b = 1, 2, 3
    color = RgbColor(r, g, b)

    assert (r, g, b) == (color.r, color.g, color.b)


@pytest.mark.parametrize('r,g,b', [
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
    (256, 0, 0),
    (0, 256, 0),
    (0, 0, 256)
])
def test_create_invalid_rgb_color(r, g, b):
    with pytest.raises(ValueError):
        RgbColor(r, g, b)


@pytest.mark.parametrize('hex_value,expected_rgb', [
    ('#00ff00', RgbColor(0, 0xff, 0)),
    ('#123abc', RgbColor(0x12, 0x3a, 0xbc)),
    ('#529988', RgbColor(0x52, 0x99, 0x88)),
    ('#90afa8', RgbColor(0x90, 0xaf, 0xa8))
])
def test_valid_hex_to_rgb_conversion_full(hex_value, expected_rgb):
    assert RgbColor.from_hex(hex_value) == expected_rgb


@pytest.mark.parametrize('hex_value,expected_rgb', [
    ('#fa1', RgbColor(0xff, 0xaa, 0x11)),
    ('#abc', RgbColor(0xaa, 0xbb, 0xcc)),
    ('#000', RgbColor(0, 0, 0)),
    ('#fff', RgbColor(0xff, 0xff, 0xff))
])
def test_valid_hex_to_rgb_conversion_short(hex_value, expected_rgb):
    assert RgbColor.from_hex(hex_value) == expected_rgb


@pytest.mark.parametrize('hex_value,expected_rgb', [
    ('#00ff00a1', RgbColor(0, 0xff, 0)),
    ('#123abc0b', RgbColor(0x12, 0x3a, 0xbc)),
    ('#52998811', RgbColor(0x52, 0x99, 0x88)),
    ('#90afa8fa', RgbColor(0x90, 0xaf, 0xa8))
])
def test_valid_hex_to_rgb_conversion_with_alpha(hex_value, expected_rgb):
    assert RgbColor.from_hex(hex_value) == expected_rgb


@pytest.mark.parametrize('hex_value,expected_rgb', [
    ('  #00ff00', RgbColor(0, 0xff, 0)),
    ('#123  ', RgbColor(0x11, 0x22, 0x33)),
    ('#529988aa\t ', RgbColor(0x52, 0x99, 0x88)),
    ('\t#90afa8   ', RgbColor(0x90, 0xaf, 0xa8))
])
def test_valid_hex_to_rgb_conversion_with_whitespace(hex_value, expected_rgb):
    assert RgbColor.from_hex(hex_value) == expected_rgb


@pytest.mark.parametrize('hex_value', ['', ' ', '\t', ' \t '])
def test_invalid_hex_to_rgb_conversion_empty_value(hex_value):
    with pytest.raises(RgbToHexConversionError):
        RgbColor.from_hex(hex_value)


@pytest.mark.parametrize('hex_value', [
    '0xffaabb', 'xfab', 'deadbeef', '00ff0211'
])
def test_invalid_hex_to_rgb_conversion_invalid_prefix(hex_value):
    with pytest.raises(RgbToHexConversionError):
        RgbColor.from_hex(hex_value)


@pytest.mark.parametrize('hex_value', [
    '#abcd', '#00ffa', '#abcdef001', '#f'
])
def test_invalid_hex_to_rgb_conversion_invalid_length(hex_value):
    with pytest.raises(RgbToHexConversionError):
        RgbColor.from_hex(hex_value)


@pytest.mark.parametrize('hex_value', [
    '#voodoo', '#aliens', '#l337ff', '#@bCd3fgh'
])
def test_invalid_hex_to_rgb_conversion_invalid_hex_value(hex_value):
    with pytest.raises(RgbToHexConversionError):
        RgbColor.from_hex(hex_value)


def test_color_equality():
    assert RgbColor(0, 0, 0) == RgbColor(0, 0, 0)
    assert RgbColor(1, 2, 3) != RgbColor(3, 2, 1)

    with pytest.raises(NotImplementedError):
        assert RgbColor(0, 0, 0) != 0


def test_rgb_color_iter():
    assert tuple(RgbColor(1, 2, 3)) == (1, 2, 3)


def test_rgb_color_to_hex():
    assert RgbColor(1, 2, 3).as_hex() == '#010203'


def test_rgb_color_to_str():
    assert str(RgbColor(1, 2, 3)) == '(1, 2, 3)'


def test_rgb_color_to_str_repr():
    assert repr(RgbColor(1, 2, 3)) == '(r=1, g=2, b=3)'


def test_rgb_color_format_str():
    color = RgbColor(1, 2, 3)

    assert f'{color}' == '(1, 2, 3)'
    assert f'{color:h}' == '#010203'
    assert f'{color:hex}' == '#010203'

    with pytest.raises(ValueError):
        f'{color:invalid_format_spec}'
