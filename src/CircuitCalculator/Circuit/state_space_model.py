from .circuit import Circuit, transform_circuit
import numpy as np
from ..Network.NodalAnalysis.state_space_model import BranchValues, nodal_state_space_model
from ..SignalProcessing.state_space_model import StateSpaceModel

def state_space_model_v2(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> StateSpaceModel:
    ssm = nodal_state_space_model(
        network=transform_circuit(circuit, w=0),
        c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in [c for c in circuit.components if c.type == 'capacitor']],
    )

    C = np.ndarray(shape=(0, ssm.n_states))
    for id in potential_nodes:
        C = np.vstack([C, ssm.c_row_for_potential(id)])
    for id in voltage_ids:
        C = np.vstack([C, ssm.c_row_voltage(id)])
    for id in current_ids:
        C = np.vstack([C, ssm.c_row_current(id)])

    D = np.ndarray(shape=(0, ssm.n_input))
    for id in potential_nodes:
        D = np.vstack([D, ssm.d_row_for_potential(id)])
    for id in voltage_ids:
        D = np.vstack([D, ssm.d_row_voltage(id)])
    for id in current_ids:
        D = np.vstack([D, ssm.d_row_current(id)])

    return StateSpaceModel(
        A=ssm.A,
        B=ssm.B,
        C=C,
        D=D
    )