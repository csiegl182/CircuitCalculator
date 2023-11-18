## Examples

### Input of circuits

Currently, there are three different ways to setup `Circuit` objects. The `Circuit` objects can then be further anaylzed.

#### Direct setup of `Circuit` objects with python code

- [DC voltage source](../test-networks/02_circuit/example_04.ipynb)
- [DC voltage and current sources](../test-networks/02_circuit/example_10.ipynb)
- [Complex elements](../test-networks/02_circuit/example_12.ipynb)

#### Load `Circuit` objects from json data files

TODO

#### Setup of `Circuit` objects via `Schematic` objects (based on schemdraw package)

- [DC voltage source](../test-networks/03_simple_circuit/example_04.ipynb)
- [DC voltage and current sources](../test-networks/03_simple_circuit/example_10.ipynb)
- [Complex elements](../test-networks/03_simple_circuit/example_12.ipynb)
- [Switches](python/example_circuit_4.ipynb)

### Analysis of circuits

CircuitCalculator provides different methods to analyse `Circuit` objects. In addition to pure python analysis, there are also predefined analyses, which create certain charts.

#### Circuit analysis

##### Bias point analysis

- [DC voltage source](../test-networks/02_circuit/example_04.ipynb)
- [DC voltage and current sources](../test-networks/02_circuit/example_10.ipynb)
- [Complex elements](../test-networks/02_circuit/example_12.ipynb)

##### Calculating open circuit resistance/impedance between two nodes

- [Open circuit resistance](../test-networks/03_circuit/example_08.ipynb)

##### Calculate parameters of Norten and Thévenin equivalent sources

TODO

#### Predefined analyses

Based on `Circuit` objects

- [Single Frequency Analysis](python/example_circuit_1.ipynb)
- [Time Domain Steady State Analysis](python/example_circuit_2.ipynb)
- [Power Flow](python/example_circuit_3.ipynb)
- [Frequency-Domain Analysis](python/example_circuit_5.ipynb)

Based on `Schematic` objects

- [Single Frequency Analysis](python/example_circuit_1.ipynb)
- [Time Domain Steady State Analysis](python/example_circuit_2.ipynb)
- [Power Flow](python/example_circuit_3.ipynb)
- [Frequency-Domain Analysis](python/example_circuit_5.ipynb)

The following examples illustrate how to use CircuitCalclulator for a DC bias point analysis on real valued resistor networks or complex valued impedance networks.

### Test Networks

For debugging and developing purposes, there exist some networks, which are also used in the automated integration tests. An overview of these examples can be found [here](test-networks/readme.md).