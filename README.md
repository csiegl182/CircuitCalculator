# CircuitCalculator

**CircuitCalculator** is a Python library for symbolic and numeric analysis of electrical circuits. It supports DC and AC analysis, nodal analysis, state-space modeling, and works with both numeric and symbolic component values. The library is designed for engineers, students, and researchers who want to analyze, simulate, or teach circuit theory using Python.

## Features

- Symbolic and numeric circuit analysis
- Support for resistors, capacitors, inductors, voltage sources, and current sources
- Nodal analysis and state-space modeling
- Easy-to-use API for building and solving circuits
- Integration with Jupyter/IPython notebooks for interactive exploration

## Installation

You can install `CircuitCalculator` and its dependencies using pip (e.g. in a virtual environment):

```bash
python -m venv ./venv
source ./venv/bin activate
pip install CircuitCalculator
```

## Usage

The most convenient interface is the Circuit class, which allows you to define a circuit as a list of components and then solve it. Below is a minimal example for DC analysis:

Example

```python
from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.Components.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

# Define the circuit
circuit = Circuit([
    ccp.dc_voltage_source(V=1, id='Vs', nodes=('1', '0')),
    ccp.resistor(R=1, id='R', nodes=('1', '0'))
])

# Solve the circuit
solution = DCSolution(circuit)
print(f'I(R)={solution.get_current("R"):2.2f}A')
print(f'V(R)={solution.get_voltage("R"):2.2f}V')
```

Output:

```
I(R)=1.00A
V(R)=1.00V
```

## Examples

Several Jupyter/IPython notebook examples can be found in the [examples](examples/) directory.

## Contribution

This project is open-source and contributions are welcome. If you would like to contribute, please fork the repository and make a pull request.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or issues, please open an issue on the GitHub repository.