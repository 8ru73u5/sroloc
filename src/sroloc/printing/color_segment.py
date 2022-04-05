from typing import Type, Dict, Union, ClassVar

from sroloc.color.ansi import BasicColor
from sroloc.color.bank import ColorBank
from sroloc.printing.color_injector import ColorInjector
from sroloc.printing.modifiers import ColorModifier, TextModifier

ModifierType = Union[ColorModifier, TextModifier]


def _get_default_modifier_keywords() -> Dict[str, ModifierType]:
    modifiers = {
        ColorModifier.bold: ['bold', 'strong', 'b'],
        ColorModifier.faint: ['faint', 'dim', 'f'],
        TextModifier.italic: ['italic', 'cursive', 'i'],
        TextModifier.underline: ['underline', 'u'],
        TextModifier.blink: ['blink', 'bl'],
        TextModifier.blink_fast: ['blink_fast', 'blf'],
        TextModifier.reverse_video: ['reverse_video', 'rv'],
        TextModifier.erase: ['erase', 'hidden', 'e'],
        TextModifier.strikethrough: ['strikethrough', 'strike', 's'],
    }

    modifier_keywords = {}
    for mod, keywords in modifiers.items():
        for k in keywords:
            modifier_keywords[k] = mod

    return modifier_keywords  # type: ignore


class ColorSegment:
    _COLOR_SCHEME: ClassVar[Type[ColorBank]] = BasicColor  # type: ignore
    COLOR_SPLITTER: ClassVar[str] = '/'
    COLOR_PLACEHOLDER: ClassVar[str] = '_'
    MODIFIER_KEYWORDS: ClassVar[Dict[str, ModifierType]] = \
        _get_default_modifier_keywords()

    def __init__(self, text: str) -> None:
        self.text = text

    @classmethod
    def set_color_scheme(cls, scheme: Type[ColorBank]) -> None:  # type: ignore
        if not issubclass(scheme, ColorBank):
            raise TypeError(
                'Color scheme must be a subclass of ColorBank, '
                f'not: {scheme.__name__!r}'
            )

        cls._COLOR_SCHEME = scheme

    def _is_token_split(self, token: str) -> bool:
        return (
                token.count(self.COLOR_SPLITTER) == 1
                and token[0] != self.COLOR_SPLITTER
                and token[-1] != self.COLOR_SPLITTER
        )

    def _validate_token(self, token: str) -> bool:
        if self._is_token_split(token):
            a, b = token.split(self.COLOR_SPLITTER)
            return self._validate_token(a) and self._validate_token(b)

        return (token in self.MODIFIER_KEYWORDS
                or self._COLOR_SCHEME.has_color(token)
                or token == self.COLOR_PLACEHOLDER)

    def _handle_modifier_token(self, modifier: ModifierType,
                               injector: ColorInjector) -> None:
        if isinstance(modifier, ColorModifier):
            injector.color_mod = modifier
        elif isinstance(modifier, TextModifier):
            injector.text_mods.add(modifier)
        else:
            raise NotImplementedError()

    def _handle_color_token(self, color: str, injector: ColorInjector) -> None:
        if self.COLOR_SPLITTER in color:
            fg_color, bg_color = color.split(self.COLOR_SPLITTER)
        else:
            fg_color = color
            bg_color = self.COLOR_PLACEHOLDER

        if fg_color != self.COLOR_PLACEHOLDER:
            injector.fg_color = fg_color

        if bg_color != self.COLOR_PLACEHOLDER:
            injector.bg_color = bg_color

    def _handle_token(self, token: str, injector: ColorInjector) -> None:
        if modifier := self.MODIFIER_KEYWORDS.get(token):
            self._handle_modifier_token(modifier, injector)
        else:
            self._handle_color_token(token, injector)

    def __format__(self, format_spec: str) -> str:
        tokens = format_spec.strip().split()

        injector = ColorInjector(self._COLOR_SCHEME)

        for token in tokens:
            if not self._validate_token(token):
                raise ValueError(
                    f'Invalid format specifier or unknown color: {token!r}'
                )

            self._handle_token(token, injector)

        return injector.apply(self.text)

    def __str__(self) -> str:
        return self.text
