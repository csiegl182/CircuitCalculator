import numpy as np
import pytest

from CircuitCalculator.Circuit.Components import components as cp
from CircuitCalculator.Network.solution import NetworkSolutionException
from CircuitCalculator.ThreePhaseCircuit import (
    NodeExpander,
    ThreePhaseCircuit,
    three_phase_complex_solution,
    three_phase_current_source_delta,
    three_phase_current_source_star,
    three_phase_custom_component_delta,
    three_phase_custom_component_line,
    three_phase_custom_component_star,
    three_phase_impedance_load_delta,
    three_phase_impedance_load_star,
    three_phase_voltage_source_delta,
    three_phase_voltage_source_star,
    transform_three_phase_circuit,
)


def test_node_expander_is_stable_for_same_phase_node() -> None:
    expander = NodeExpander()
    first = expander.phase_node("N1", "a")
    second = expander.phase_node("N1", "a")
    assert first == "N1.a"
    assert second == first


def test_transform_three_phase_circuit_expands_star_components() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            three_phase_voltage_source_star(id="V1", nodes=("SRC", "N"), V=230 + 0j),
            three_phase_impedance_load_star(id="Z1", nodes=("SRC", "N"), Z=10 + 5j),
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
            three_phase_voltage_source_delta(id="Vd", nodes=("BUS",), V=400 + 0j),
            three_phase_impedance_load_delta(id="Zd", nodes=("BUS",), Z=20 + 10j),
        ]
    )

    circuit = transform_three_phase_circuit(three_phase)

    assert len(circuit.components) == 6
    ids = [component.id for component in circuit.components]
    assert set(ids) == {"Vd.ab", "Vd.bc", "Vd.ca", "Zd.ab", "Zd.bc", "Zd.ca"}


def test_three_phase_sources_use_default_phase_shift() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            three_phase_voltage_source_star(id="Vy", nodes=("BUSY", "N"), V=230 + 0j),
            three_phase_voltage_source_delta(id="Vd", nodes=("BUSD",), V=400 + 0j),
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


def test_three_phase_current_sources_use_default_phase_shift() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            three_phase_current_source_star(id="Iy", nodes=("BUSY", "N"), I=10 + 0j),
            three_phase_current_source_delta(id="Id", nodes=("BUSD",), I=15 + 0j),
        ],
        ground_node="N",
    )
    circuit = transform_three_phase_circuit(three_phase)
    by_id = {component.id: component for component in circuit.components}

    iy_a = complex(by_id["Iy.a"].value["I_real"], by_id["Iy.a"].value["I_imag"])
    iy_b = complex(by_id["Iy.b"].value["I_real"], by_id["Iy.b"].value["I_imag"])
    iy_c = complex(by_id["Iy.c"].value["I_real"], by_id["Iy.c"].value["I_imag"])
    id_ab = complex(by_id["Id.ab"].value["I_real"], by_id["Id.ab"].value["I_imag"])
    id_bc = complex(by_id["Id.bc"].value["I_real"], by_id["Id.bc"].value["I_imag"])
    id_ca = complex(by_id["Id.ca"].value["I_real"], by_id["Id.ca"].value["I_imag"])

    assert np.isclose(iy_a, 10 + 0j)
    assert np.isclose(iy_b, 10 * np.exp(-1j * 2 * np.pi / 3))
    assert np.isclose(iy_c, 10 * np.exp(1j * 2 * np.pi / 3))
    assert np.isclose(id_ab, 15 + 0j)
    assert np.isclose(id_bc, 15 * np.exp(-1j * 2 * np.pi / 3))
    assert np.isclose(id_ca, 15 * np.exp(1j * 2 * np.pi / 3))


def test_three_phase_custom_component_supports_line_topology() -> None:
    line = three_phase_custom_component_line(
        id="L1",
        nodes=("SRC", "LOAD"),
        phase_a=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=0.1 + 0.2j),
        phase_b=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=0.1 + 0.2j),
        phase_c=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=0.1 + 0.2j),
    )
    circuit = transform_three_phase_circuit(ThreePhaseCircuit(components=[line]))
    by_id = {component.id: component for component in circuit.components}

    assert by_id["L1.a"].nodes == ("SRC.a", "LOAD.a")
    assert by_id["L1.b"].nodes == ("SRC.b", "LOAD.b")
    assert by_id["L1.c"].nodes == ("SRC.c", "LOAD.c")


def test_three_phase_custom_component_supports_star_and_delta_topology() -> None:
    star = three_phase_custom_component_star(
        id="CS",
        nodes=("BUS", "N"),
        phase_a=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 1j),
        phase_b=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=2 + 2j),
        phase_c=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=3 + 3j),
    )
    delta = three_phase_custom_component_delta(
        id="CD",
        nodes=("BUS2",),
        phase_a=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
        phase_b=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
        phase_c=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
    )
    circuit = transform_three_phase_circuit(ThreePhaseCircuit(components=[star, delta], ground_node="N"))
    by_id = {component.id: component for component in circuit.components}

    assert by_id["CS.a"].nodes == ("BUS.a", "N.n")
    assert by_id["CS.b"].nodes == ("BUS.b", "N.n")
    assert by_id["CS.c"].nodes == ("BUS.c", "N.n")
    assert by_id["CD.ab"].nodes == ("BUS2.a", "BUS2.b")
    assert by_id["CD.bc"].nodes == ("BUS2.b", "BUS2.c")
    assert by_id["CD.ca"].nodes == ("BUS2.c", "BUS2.a")


def test_three_phase_complex_solution_runs_for_balanced_star_case() -> None:
    three_phase = ThreePhaseCircuit(
        components=[
            three_phase_voltage_source_star(id="V1", nodes=("SRC", "N"), V=230 + 0j, Z=0.2 + 0.1j),
            three_phase_impedance_load_star(id="Z1", nodes=("SRC", "N"), Z=15 + 4j),
        ],
        ground_node="N",
    )

    solution = three_phase_complex_solution(three_phase, w=2 * np.pi * 50)

    assert np.isfinite(solution.get_current("V1.a").real)
    assert np.isfinite(solution.get_current("V1.b").real)
    assert np.isfinite(solution.get_current("V1.c").real)


def test_invalid_nodes_raise_node_mapping_error() -> None:
    from CircuitCalculator.ThreePhaseCircuit.components import NodeMappingError

    invalid_components = [
        three_phase_voltage_source_star(id="Vs", nodes=("BUS",), V=230 + 0j),
        three_phase_voltage_source_delta(id="Vd", nodes=("BUS", "N"), V=400 + 0j),
        three_phase_current_source_star(id="Is", nodes=("BUS",), I=10 + 0j),
        three_phase_current_source_delta(id="Id", nodes=("BUS", "N"), I=10 + 0j),
        three_phase_impedance_load_star(id="Zs", nodes=("BUS",), Z=10 + 5j),
        three_phase_impedance_load_delta(id="Zd", nodes=("BUS", "N"), Z=10 + 5j),
        three_phase_custom_component_line(
            id="L", nodes=("ONLY_ONE",),
            phase_a=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
            phase_b=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
            phase_c=lambda cid, nd: cp.impedance(id=cid, nodes=nd, Z=1 + 0j),
        ),
    ]

    for component in invalid_components:
        with pytest.raises(NodeMappingError):
            transform_three_phase_circuit(ThreePhaseCircuit(components=[component]))


def test_node_expander_collision_uses_short_suffix() -> None:
    expander = NodeExpander()
    expander._allocated.add("BUS.a")
    node = expander.phase_node("BUS", "a")
    assert node == "BUS.a_2"


def test_three_phase_complex_solution_returns_nan_on_solver_conflict() -> None:
    circuit = ThreePhaseCircuit(
        components=[
            three_phase_current_source_delta(id="Id", nodes=("BUS",), I=12 + 0j),
            three_phase_impedance_load_delta(id="Zd", nodes=("BUS",), Z=25 + 10j),
        ]
    )

    def failing_solver(_):
        raise NetworkSolutionException("conflict", contradictional_elements=("Id.ab",))

    solution = three_phase_complex_solution(circuit, w=2 * np.pi * 50, solver=failing_solver)

    assert np.isnan(solution.get_current("Id.ab"))
    assert np.isnan(solution.get_voltage("Zd.ab"))
