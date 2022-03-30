from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Generic, Optional

from sroloc.color.utils import UnknownColorError

ColorType = TypeVar('ColorType')


class ColorBank(Generic[ColorType], ABC):
    _DEFAULT_COLOR: Optional[ColorType] = None
    _BANK: Dict[str, ColorType]

    @classmethod
    def set_default_color(cls, color: ColorType) -> None:
        cls._DEFAULT_COLOR = color

    @classmethod
    def set_default_color_from_bank(cls, color_name: str) -> None:
        cls._DEFAULT_COLOR = cls.get_color(color_name)

    @classmethod
    def add_color_to_bank(cls, name: str, color: ColorType) -> None:
        cls._BANK[name] = color

    @classmethod
    def get_color(cls, name: str) -> ColorType:
        try:
            return cls._BANK[name]  # type: ignore
        except KeyError:
            if cls._DEFAULT_COLOR:
                return cls._DEFAULT_COLOR  # type: ignore

            raise UnknownColorError(name)

    @classmethod
    def has_color(cls, name: str) -> bool:
        return name in cls._BANK

    @classmethod
    @abstractmethod
    def fg_color_code(cls, color: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def bg_color_code(cls, color: str) -> str:
        pass
