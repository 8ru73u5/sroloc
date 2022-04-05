import pytest

from sroloc.color.true import TrueColor
from sroloc.printing.color_injector import ColorInjector
from sroloc.printing.color_segment import ColorSegment
from sroloc.printing.modifiers import ColorModifier, TextModifier


@pytest.fixture(scope='function')
def default_segment():
    previous_color_scheme = ColorSegment._COLOR_SCHEME
    previous_color_splitter = ColorSegment.COLOR_SPLITTER
    previous_color_placeholder = ColorSegment.COLOR_PLACEHOLDER
    previous_modifier_keywords = ColorSegment.MODIFIER_KEYWORDS

    ColorSegment._COLOR_SCHEME = TrueColor
    ColorSegment.COLOR_SPLITTER = '/'
    ColorSegment.COLOR_PLACEHOLDER = '_'
    ColorSegment.MODIFIER_KEYWORDS = {
        'bold': ColorModifier.bold,
        'faint': ColorModifier.faint,
        'italic': TextModifier.italic,
        'underline': TextModifier.underline,
        'blink': TextModifier.blink,
        'blink_fast': TextModifier.blink_fast,
        'reverse_video': TextModifier.reverse_video,
        'erase': TextModifier.erase,
        'strikethrough': TextModifier.strikethrough,
    }

    yield ColorSegment('test')

    ColorSegment._COLOR_SCHEME = previous_color_scheme
    ColorSegment.COLOR_SPLITTER = previous_color_splitter
    ColorSegment.COLOR_PLACEHOLDER = previous_color_placeholder
    ColorSegment.MODIFIER_KEYWORDS = previous_modifier_keywords


@pytest.fixture(scope='function')
def default_injector():
    return ColorInjector(TrueColor)


def test_setting_valid_color_scheme():
    class LameColorScheme(TrueColor):
        pass

    ColorSegment.set_color_scheme(LameColorScheme)

    assert ColorSegment._COLOR_SCHEME == LameColorScheme


def test_setting_invalid_color_scheme():
    with pytest.raises(TypeError):
        ColorSegment.set_color_scheme(str)  # type: ignore


@pytest.mark.parametrize('value,expected_result', [
    ('value1/value2', True),
    ('value/', False),
    ('/value', False),
    ('/', False),
    ('value', False)
])
def test_checking_for_split_token(default_segment, value, expected_result):
    assert default_segment._is_token_split(value) is expected_result


@pytest.mark.parametrize('value,expected_result', [
    ('#fff/#000', True),
    ('_/#1a2b3c', True),
    ('#3c2b1a/_', True),
    ('invalid_color/invalid_color', False),
    ('_/invalid_color', False),
    ('invalid_color/_', False),
    ('_/_', True),
    ('/#fff', False),
    ('#fff/', False),
    ('/', False)
])
def test_validating_split_color_token(default_segment, value, expected_result):
    assert default_segment._validate_token(value) is expected_result


@pytest.mark.parametrize('value,expected_result', [
    ('#fff', True),
    ('_', True),
    ('invalid_color', False)
])
def test_validating_color_token(default_segment, value, expected_result):
    assert default_segment._validate_token(value) is expected_result


def test_validating_modifier_token(default_segment):
    assert default_segment._validate_token('bold') is True
    assert default_segment._validate_token('unknown_modifier') is False


def test_adding_one_color_modifier(default_segment, default_injector):
    modifier = ColorModifier.bold
    default_segment._handle_modifier_token(modifier, default_injector)

    assert default_injector.color_mod is modifier


def test_adding_multiple_color_modifiers(default_segment, default_injector):
    modifiers = [
        ColorModifier.bold,
        ColorModifier.reset,
        ColorModifier.faint
    ]

    for modifier in modifiers:
        default_segment._handle_modifier_token(modifier, default_injector)

    assert default_injector.color_mod is modifiers[-1]


def test_adding_one_text_modifier(default_segment, default_injector):
    modifier = TextModifier.italic
    default_segment._handle_modifier_token(modifier, default_injector)

    assert default_injector.text_mods == {modifier}


def test_adding_multiple_text_modifiers(default_segment, default_injector):
    modifiers = {
        TextModifier.italic,
        TextModifier.strikethrough,
        TextModifier.reverse_video
    }

    for modifier in modifiers:
        default_segment._handle_modifier_token(modifier, default_injector)

    assert default_injector.text_mods == modifiers


def test_adding_no_modifiers(default_injector):
    assert len(default_injector.text_mods) == 0
    assert default_injector.color_mod is None


@pytest.mark.parametrize('value', ['bold', 'something', 1, list()])
def test_adding_invalid_modifier(default_segment, default_injector, value):
    with pytest.raises(NotImplementedError):
        default_segment._handle_modifier_token(
            value, default_injector  # type: ignore
        )


def test_adding_one_fg_color(default_segment, default_injector):
    color = '#fff'
    default_segment._handle_color_token(color, default_injector)

    assert default_injector.fg_color == color
    assert default_injector.bg_color is None


def test_adding_multiple_fg_colors(default_segment, default_injector):
    expected_color = '#1a2b3c'
    colors = ['#fff', '#000', expected_color]

    for color in colors:
        default_segment._handle_color_token(color, default_injector)

    assert default_injector.fg_color == expected_color
    assert default_injector.bg_color is None


def test_adding_one_split_color(default_segment, default_injector):
    fg_color = '#fff'
    bg_color = '#000'
    color = f'{fg_color}/{bg_color}'

    default_segment._handle_color_token(color, default_injector)

    assert default_injector.fg_color == fg_color
    assert default_injector.bg_color == bg_color


def test_adding_multiple_split_colors(default_segment, default_injector):
    expected_fg_color = '#1a2b3c'
    expected_bg_color = '#4d5e6f'

    color_pairs = [
        ('#fff', '#000'),
        ('#123', '#321'),
        (expected_fg_color, expected_bg_color)
    ]

    for fg_color, bg_color in color_pairs:
        color = f'{fg_color}/{bg_color}'
        default_segment._handle_color_token(color, default_injector)

    assert default_injector.fg_color == expected_fg_color
    assert default_injector.bg_color == expected_bg_color


def test_adding_mix_split_and_single_colors(default_segment, default_injector):
    expected_fg_color = '#1a2b3c'
    expected_bg_color = '#4d5e6f'

    color_tokens = [
        '#fff',
        '#abcdef',
        '#aaa/#bbb',
        '#420',
        f'#ccc/{expected_bg_color}',
        '#dead69',
        expected_fg_color
    ]

    for color_token in color_tokens:
        default_segment._handle_color_token(color_token, default_injector)

    assert default_injector.fg_color == expected_fg_color
    assert default_injector.bg_color == expected_bg_color


def test_handling_tokens(default_segment, default_injector):
    expected_color_modifier = ColorModifier.bold
    expected_text_modifiers = {TextModifier.italic, TextModifier.blink}
    expected_fg_color = '#1a2b3c'
    expected_bg_color = '#4d5e6f'
    tokens = [
        'faint',
        'italic',
        '#111',
        '_/#fff',
        'bold',
        f'{expected_fg_color}/{expected_bg_color}',
        'blink'
    ]

    for token in tokens:
        default_segment._handle_token(token, default_injector)

    assert default_injector.fg_color == expected_fg_color
    assert default_injector.bg_color == expected_bg_color
    assert default_injector.color_mod is expected_color_modifier
    assert default_injector.text_mods == expected_text_modifiers


@pytest.mark.parametrize('format_string', [
    'invalid_modifier #fff',
    'bold italic invalid_color',
    'invalid_modifier invalid_color'
])
def test_invalid_format_string(default_segment, format_string):
    with pytest.raises(ValueError):
        f'{default_segment:{format_string}}'


def test_empty_format_string(default_segment):
    assert f'{default_segment:}' == default_segment.text


def test_default_colors_format_string(default_segment):
    assert f'{default_segment:_}' == default_segment.text
    assert f'{default_segment:_/_}' == default_segment.text


def test_converting_to_string():
    value = 'test'
    cs = ColorSegment(value)

    assert str(cs) == value
