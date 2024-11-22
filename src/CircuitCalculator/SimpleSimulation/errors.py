from functools import wraps

class UnknownCircuitElement(Exception):
    def __init__(self, element_type: str) -> None:
        super().__init__(f'Unknown circuit element type "{element_type}".')
        self.element_type = element_type

class MissingArgument(Exception):
    def __init__(self, missing_argument: str, provided_arguments: str) -> None:
        super().__init__(f'Missing argument: {missing_argument}. Given arguments: {provided_arguments}.')
        self.missing = missing_argument
        self.provided_arguments = provided_arguments

class IllegalElementValue(Exception): ...

simulation_exceptions : tuple[type[Exception], ...] = (
    UnknownCircuitElement,
    MissingArgument,
    IllegalElementValue
)