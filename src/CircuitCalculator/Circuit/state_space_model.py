from .circuit import Circuit, transform_circuit
from ..Network.NodalAnalysis import state_space_model as ssm
from ..SignalProcessing.state_space_model import NumericStateSpaceModel
from typing import Protocol

import numpy as np
from dataclasses import dataclass

class CircuitStateSpaceModel(Protocol):
    @property
    def A(self) -> np.ndarray: ...
    @property
    def B(self) -> np.ndarray: ...

    def C(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> np.ndarray: ...

    def D(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> np.ndarray: ...

    def c_d_row_for_potential(self, node_id: str) -> tuple[np.ndarray, np.ndarray]: ...

    def c_d_row_for_voltage(self, node_id: str) -> tuple[np.ndarray, np.ndarray]: ...

    def c_d_row_for_current(self, node_id: str) -> tuple[np.ndarray, np.ndarray]: ...

@dataclass
class NumericCircuitStateSpaceModel(CircuitStateSpaceModel):

    def __init__(self, circuit: Circuit) -> None:
        self._network = transform_circuit(circuit, w=0)
        self._state_space_model = ssm.numeric_state_space_model(
            network=self._network,
            c_values={C.id : float(C.value['C']) for C in [c for c in circuit.components if c.type == 'capacitor']},
            l_values={L.id : float(L.value['L']) for L in [c for c in circuit.components if c.type == 'inductance']}
        )

    @property
    def A(self) -> np.ndarray:
        return self._state_space_model.A

    @property
    def B(self) -> np.ndarray:
        return self._state_space_model.B

    def C(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> np.ndarray:
        return self._state_space_model.extend_C_matrix(potential_nodes, voltage_ids, current_ids)

    def D(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> np.ndarray:
        return self._state_space_model.extend_D_matrix(potential_nodes, voltage_ids, current_ids)

    def c_d_row_for_potential(self, node_id: str) -> tuple[np.ndarray, np.ndarray]:
        return self._state_space_model.c_row_for_potential(node_id), self._state_space_model.d_row_for_potential(node_id)

    def c_d_row_for_voltage(self, node_id: str) -> tuple[np.ndarray, np.ndarray]:
        return self._state_space_model.c_row_voltage(node_id), self._state_space_model.d_row_voltage(node_id)

    def c_d_row_for_current(self, node_id: str) -> tuple[np.ndarray, np.ndarray]:
        return self._state_space_model.c_row_current(node_id), self._state_space_model.d_row_current(node_id)

    @property
    def sources(self) -> list[str]:
        return self._state_space_model.sources()

def state_space_model(circuit: Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> NumericStateSpaceModel:
    state_space_model = NumericCircuitStateSpaceModel(circuit)
    return NumericStateSpaceModel(
        A=state_space_model.A,
        B=state_space_model.B,
        C=state_space_model.C(potential_nodes, voltage_ids, current_ids),
        D=state_space_model.D(potential_nodes, voltage_ids, current_ids)
    )