from .circuit import Circuit, transform_circuit
import numpy as np
from ..Network.NodalAnalysis.state_space_model import nodal_state_space_model
from ..SignalProcessing.state_space_model import StateSpaceModel

def state_space_model(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> StateSpaceModel:
    ssm = nodal_state_space_model(
        network=transform_circuit(circuit, w=0),
        c_values={C.id : float(C.value['C']) for C in [c for c in circuit.components if c.type == 'capacitor']},
        l_values={L.id : float(L.value['L']) for L in [c for c in circuit.components if c.type == 'inductance']}
    )

    C = np.ndarray(shape=(0, ssm.n_states))
    for id in potential_nodes:
        C = np.vstack([C, ssm.c_row_for_potential(id)])
    for id in voltage_ids:
        C = np.vstack([C, ssm.c_row_voltage(id)])
    for id in current_ids:
        C = np.vstack([C, ssm.c_row_current(id)])

    D = np.ndarray(shape=(0, ssm.n_inputs))
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