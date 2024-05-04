from .circuit import Circuit, transform_circuit
import numpy as np
from ..Network.NodalAnalysis.state_space_model import NodalStateSpaceModel, BranchValues, Output, OutputType
from ..SignalProcessing.state_space_model import StateSpaceModel


def state_space_model(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> StateSpaceModel:
    nodal_state_space_model = NodalStateSpaceModel(
        network=transform_circuit(circuit, w=0),
        c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in [c for c in circuit.components if c.type == 'capacitor']],
        output_values=[Output(OutputType.POTENTIAL, id) for id in potential_nodes] + [Output(OutputType.VOLTAGE, id) for id in voltage_ids] + [Output(OutputType.CURRENT, id) for id in current_ids]
    )
    return StateSpaceModel(
        A=nodal_state_space_model.A,
        B=nodal_state_space_model.B,
        C=nodal_state_space_model.C,
        D=nodal_state_space_model.D,
    )