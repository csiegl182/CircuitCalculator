import json
import numpy as np

from CircuitCalculator.Circuit.dump_load import deserialize, serialize
from CircuitCalculator.Circuit.solution import complex_solution
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import components as cp


def test_complex_admittance_json_can_be_deserialized_and_analyzed() -> None:
    data = {
        "components": [
            {
                "type": "complex_voltage_source",
                "id": "Vs",
                "nodes": ["1", "0"],
                "value": {
                    "V": {
                        "__complex__": True,
                        "real": 12.0,
                        "imag": 0.0,
                    }
                },
            },
            {
                "type": "admittance",
                "id": "Y1",
                "nodes": ["1", "0"],
                "value": {
                    "G": 0.125,
                    "B": 0.0,
                },
            },
        ],
        "ground_node": "0",
    }

    circuit = deserialize(json.dumps(data), "json")
    solution = complex_solution(circuit, w=2 * np.pi * 50)

    assert np.isclose(solution.get_voltage("Vs"), 12 + 0j)
    assert np.isclose(solution.get_current("Y1"), 1.5 + 0j)


def test_numeric_complex_admittance_survives_circuit_json_roundtrip() -> None:
    circuit = Circuit(
        [cp.admittance(id="Y1", nodes=("1", "0"), Y=0.125 + 0.25j)],
        ground_node="0",
    )

    loaded = deserialize(serialize(circuit, "json"), "json")

    assert loaded.ground_node == "0"
    assert loaded["Y1"].value["G"] == 0.125
    assert loaded["Y1"].value["B"] == 0.25


def test_admittance_is_serialized_in_cartesian_form_like_impedance() -> None:
    circuit = Circuit(
        [
            cp.impedance(id="Z1", nodes=("1", "0"), Z=10 + 5j),
            cp.admittance(id="Y1", nodes=("1", "0"), Y=0.125 + 0.25j),
        ],
        ground_node="0",
    )

    serialized = json.loads(serialize(circuit, "json"))

    assert serialized["components"][0]["value"] == {"R": 10.0, "X": 5.0}
    assert serialized["components"][1]["value"] == {"G": 0.125, "B": 0.25}
