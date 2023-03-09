from typing import TypeVar, Callable, Any, Type
import schemdraw.elements

SchemdrawElement = TypeVar('SchemdrawElement', bound=schemdraw.elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, tuple[str, ...]], Any]

ElementTranslatorMap = dict[Type[schemdraw.elements.Element], SchemdrawElementTranslator]