from .circuit import Circuit, transform_circuit
import numpy as np
from ..Network.NodalAnalysis.state_space_model import NodalStateSpaceModel, BranchValues, Output, OutputType, state_space_matrices_for_potentials, new_state_space_model
from ..SignalProcessing.state_space_model import StateSpaceModel


def state_space_model(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> StateSpaceModel:
    nodal_state_space_model = NodalStateSpaceModel(
        network=transform_circuit(circuit, w=0),
        c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in [c for c in circuit.components if c.type == 'capacitor']],
        output_values=[Output(OutputType.POTENTIAL, id) for id in potential_nodes] + [Output(OutputType.VOLTAGE, id) for id in voltage_ids] + [Output(OutputType.CURRENT, id) for id in current_ids]
    )
    A, B, C, D = state_space_matrices_for_potentials(
        network=transform_circuit(circuit, w=0),
        c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in [c for c in circuit.components if c.type == 'capacitor']]
    )
    return StateSpaceModel(
        A=nodal_state_space_model.A,
        B=nodal_state_space_model.B,
        C=nodal_state_space_model.C,
        D=nodal_state_space_model.D,
    )

def state_space_model_v2(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> StateSpaceModel:
    nodal_state_space_model = new_state_space_model(
        network=transform_circuit(circuit, w=0),
        c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in [c for c in circuit.components if c.type == 'capacitor']],
    )

    C = np.ndarray(shape=(0, nodal_state_space_model.n_states))
    for id in potential_nodes:
        C = np.vstack([C, nodal_state_space_model.c_row_for_potential(id)])
    for id in voltage_ids:
        C = np.vstack([C, nodal_state_space_model.c_row_voltage(id)])
    for id in current_ids:
        C = np.vstack([C, nodal_state_space_model.c_row_current(id)])

    D = np.ndarray(shape=(0, nodal_state_space_model.n_input))
    for id in potential_nodes:
        D = np.vstack([D, nodal_state_space_model.d_row_for_potential(id)])
    for id in voltage_ids:
        D = np.vstack([D, nodal_state_space_model.d_row_voltage(id)])
    for id in current_ids:
        D = np.vstack([D, nodal_state_space_model.d_row_current(id)])

    return StateSpaceModel(
        A=nodal_state_space_model.A,
        B=nodal_state_space_model.B,
        C=C,
        D=D
    )