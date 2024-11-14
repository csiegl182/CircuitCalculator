from functools import wraps

class UnknownCircuitElement(Exception): ...
class MissingArguments(Exception): ...

simulation_exceptions : tuple[type[Exception], ...] = (
    UnknownCircuitElement,
    MissingArguments
)

def handle_simulation_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except simulation_exceptions as e:
            print(e)
            return
    return wrapper