import numpy as np

from CircuitCalculator.ThreePhaseCircuit import (
    NodeExpander,
    ThreePhaseCircuit,
    ThreePhaseLoadDelta,
    ThreePhaseLoadY,
    ThreePhaseVoltageSourceDelta,
    ThreePhaseVoltageSourceY,
    three_phase_complex_solution,
    transform_three_phase_circuit,
)


def test_node_expander_is_stable_for_same_phase_node() -> None:
    expander = NodeExpander()
    first = expander.phase_node("N1", "a")
    second = expander.phase_node("N1", "a")
    assert first == "N1.a"
    assert second == first


def test_transform_three_phase_circuit_expands_y_components() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            ThreePhaseVoltageSourceY(id="V1", nodes=("SRC", "N"), V=230 + 0j),
            ThreePhaseLoadY(id="Z1", nodes=("SRC", "N"), Z=10 + 5j),
        ],
        ground_node="N",
    )

    circuit = transform_three_phase_circuit(three_phase)

    assert len(circuit.components) == 6
    assert circuit.ground_node == "N.n"
    ids = [component.id for component in circuit.components]
    assert "V1.a" in ids
    assert "V1.b" in ids
    assert "V1.c" in ids
    assert "Z1.a" in ids
    assert "Z1.b" in ids
    assert "Z1.c" in ids


def test_transform_three_phase_circuit_expands_delta_components() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            ThreePhaseVoltageSourceDelta(id="Vd", nodes=("BUS",), V=400 + 0j),
            ThreePhaseLoadDelta(id="Zd", nodes=("BUS",), Z=20 + 10j),
        ]
    )

    circuit = transform_three_phase_circuit(three_phase)

    assert len(circuit.components) == 6
    ids = [component.id for component in circuit.components]
    assert set(ids) == {"Vd.ab", "Vd.bc", "Vd.ca", "Zd.ab", "Zd.bc", "Zd.ca"}

def test_three_phase_sources_use_default_phase_shift() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            ThreePhaseVoltageSourceY(id="Vy", nodes=("BUSY", "N"), V=230 + 0j),
            ThreePhaseVoltageSourceDelta(id="Vd", nodes=("BUSD",), V=400 + 0j),
        ],
        ground_node="N",
    )
    circuit = transform_three_phase_circuit(three_phase)
    by_id = {component.id: component for component in circuit.components}

    vy_a = complex(by_id["Vy.a"].value["V_real"], by_id["Vy.a"].value["V_imag"])
    vy_b = complex(by_id["Vy.b"].value["V_real"], by_id["Vy.b"].value["V_imag"])
    vy_c = complex(by_id["Vy.c"].value["V_real"], by_id["Vy.c"].value["V_imag"])
    vd_ab = complex(by_id["Vd.ab"].value["V_real"], by_id["Vd.ab"].value["V_imag"])
    vd_bc = complex(by_id["Vd.bc"].value["V_real"], by_id["Vd.bc"].value["V_imag"])
    vd_ca = complex(by_id["Vd.ca"].value["V_real"], by_id["Vd.ca"].value["V_imag"])

    assert np.isclose(vy_a, 230 + 0j)
    assert np.isclose(vy_b, 230 * np.exp(-1j * 2 * np.pi / 3))
    assert np.isclose(vy_c, 230 * np.exp(1j * 2 * np.pi / 3))
    assert np.isclose(vd_ab, 400 + 0j)
    assert np.isclose(vd_bc, 400 * np.exp(-1j * 2 * np.pi / 3))
    assert np.isclose(vd_ca, 400 * np.exp(1j * 2 * np.pi / 3))


def test_three_phase_complex_solution_runs_for_balanced_y_case() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            ThreePhaseVoltageSourceY(id="V1", nodes=("SRC", "N"), V=230 + 0j, Z=0.2 + 0.1j),
            ThreePhaseLoadY(id="Z1", nodes=("SRC", "N"), Z=15 + 4j),
        ],
        ground_node="N",
    )

    solution = three_phase_complex_solution(three_phase, w=2 * np.pi * 50)

    assert np.isfinite(solution.get_current("V1.a").real)
    assert np.isfinite(solution.get_current("V1.b").real)
    assert np.isfinite(solution.get_current("V1.c").real)
