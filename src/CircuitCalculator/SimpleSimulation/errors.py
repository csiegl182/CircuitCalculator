from CircuitCalculator.Circuit.circuit import AmbiguousComponentID
from CircuitCalculator.dump_load import FormatError

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

class UnknownSolutionType(Exception):
    def __init__(self, solution_type: str, available_solutions: list[str]) -> None:
        super().__init__(f'Unknown solution type "{solution_type}". Available solutions: {", ".join(available_solutions)}.')
        self.solution_type = solution_type
        self.available_solutions = available_solutions

class SolutionUsageError(Exception):
    def __init__(self, solution_type: str, unknown_arguments: list[str]) -> None:
        error_message = f'Cannot use solution "{solution_type}" with arguments: {", ".join(unknown_arguments)}.'
        if len(unknown_arguments) == 0:
            error_message = f'Cannot use solution "{solution_type}".'
        if len(unknown_arguments) == 1:
            error_message = f'Cannot use solution "{solution_type}" with argument: {unknown_arguments[0]}.'
        super().__init__(error_message)
        self.solution_type = solution_type
        self.unknown_arguments = unknown_arguments

class IllegalElementValue(Exception): ...

class EmptyCircuit(Exception): ...

simulation_exceptions : tuple[type[Exception], ...] = (
    UnknownCircuitElement,
    MissingArgument,
    IllegalElementValue,
    UnknownArgument,
    AmbiguousComponentID,
    FileNotFoundError,
    FormatError,
    UnknownSolutionType,
    SolutionUsageError,
    EmptyCircuit,
    KeyError
)