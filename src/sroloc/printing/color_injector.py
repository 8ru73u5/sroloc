from dataclasses import dataclass, field
from typing import Type, Optional, Set, List

from sroloc.color.bank import ColorBank
from sroloc.printing.modifiers import ColorModifier, TextModifier


@dataclass
class ColorInjector:
    color_scheme: Type[ColorBank]  # type: ignore
    fg_color: Optional[str] = None
    bg_color: Optional[str] = None
    color_mod: Optional[ColorModifier] = None
    text_mods: Set[TextModifier] = field(default_factory=set)

    def apply(self, text: str) -> str:
        elements: List[str] = []

        if self.color_mod:
            elements.append(str(self.color_mod.value))

        if self.fg_color:
            color_code = self.color_scheme.fg_color_code(self.fg_color)
            elements.append(color_code)

        if self.bg_color:
            color_code = self.color_scheme.bg_color_code(self.bg_color)
            elements.append(color_code)

        for mod in self.text_mods:
            elements.append(str(mod.value))

        if not elements:
            return text

        color_sequence = ';'.join(elements)

        return f'\x1b[{color_sequence}m{text}\x1b[0m'
