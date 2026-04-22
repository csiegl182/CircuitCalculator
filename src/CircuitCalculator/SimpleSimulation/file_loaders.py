from CircuitCalculator.dump_load import load, ParseError


def load_simulation_file(name: str) -> dict:
    try:
        return load(name)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'Simulation file "{name}" does not exist.') from e
    except ParseError as e:
        raise ParseError(f'Cannot parse "{name}" as simulation file due to format issues.') from e
