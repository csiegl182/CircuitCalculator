from CircuitCalculator.Circuit.transfer_function import numeric_transfer_function, TransferFunctionOutput
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import components as cmp


R = 10.0
C = 2e-3

circuit = Circuit(
    components=[
        cmp.dc_voltage_source(id="Vs", V=1.0, nodes=("1", "0")),
        cmp.resistor(id="R1", R=R, nodes=("1", "2")),
        cmp.capacitor(id="C1", C=C, nodes=("2", "0")),
    ],
    ground_node="0",
)

tf = numeric_transfer_function(
    circuit,
    input_id="Vs",
    output=TransferFunctionOutput.voltage("C1"),
)

print("Numerator coefficients:", tf.numerator_coeffs)
print("Denominator coefficients:", tf.denominator_coeffs)
print("Poles:", tf.poles())
print("Zeros:", tf.zeros())
print("SciPy transfer function:", tf.transfer_function())
