from functools import wraps
from CircuitCalculator.Circuit.circuit import AmbiguousComponentID

class UnknownCircuitElement(Exception):
    def __init__(self, element_type: str) -> None:
        super().__init__(f'Unknown circuit element type "{element_type}".')
        self.element_type = element_type

class MissingArgument(Exception):
    def __init__(self, missing_argument: str, provided_arguments: str) -> None:
        super().__init__(f'Missing argument: {missing_argument}. Given arguments: {provided_arguments}.')
        self.missing = missing_argument
        self.provided_arguments = provided_arguments

class UnknownArgument(Exception):
    def __init__(self, unknown_argument: str, method: str = '') -> None:
        super().__init__(f"Unknown argument {unknown_argument}" + f" for method '{method}'." if len(method) > 0 else '.')
        self.unknown_argument = unknown_argument
        self.method = method

class IllegalElementValue(Exception): ...

simulation_exceptions : tuple[type[Exception], ...] = (
    UnknownCircuitElement,
    MissingArgument,
    IllegalElementValue,
    UnknownArgument,
    AmbiguousComponentID
)