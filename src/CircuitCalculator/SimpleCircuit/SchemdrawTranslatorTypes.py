from typing import TypeVar, Callable, Type
import schemdraw.elements
from ..Circuit.Components.components import Component

SchemdrawElement = TypeVar('SchemdrawElement', bound=schemdraw.elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, tuple[str, ...]], Component | None] | Callable[[SchemdrawElement, tuple[str, ...]], Component | None]

ElementTranslatorMap = dict[Type[schemdraw.elements.Element], SchemdrawElementTranslator]