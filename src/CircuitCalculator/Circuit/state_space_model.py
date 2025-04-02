from . import circuit as cc
from ..Network.NodalAnalysis import state_space_model as ssm
from ..SignalProcessing.state_space_model import NumericStateSpaceModel, SymbolicStateSpaceModel
from typing import Any

import numpy as np
import sympy as sp
from dataclasses import dataclass

@dataclass
class StateSpaceMatrixConstructor:

    _state_space_model: ssm.StateSpaceGenericOutput

    @property
    def A(self) -> Any:
        return self._state_space_model.A
    
    @property
    def B(self) -> Any:
        return self._state_space_model.B

    def C(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> Any:
        return self._state_space_model.extend_C_matrix(potential_nodes, voltage_ids, current_ids)

    def D(self, potential_nodes: list[str], voltage_ids: list[str], current_ids: list[str]) -> Any:
        return self._state_space_model.extend_D_matrix(potential_nodes, voltage_ids, current_ids)

    def c_d_row_for_potential(self, node_id: str) -> tuple[Any, Any]:
        return self._state_space_model.c_row_for_potential(node_id), self._state_space_model.d_row_for_potential(node_id)

    def c_d_row_for_voltage(self, node_id: str) -> tuple[Any, Any]:
        return self._state_space_model.c_row_voltage(node_id), self._state_space_model.d_row_voltage(node_id)

    def c_d_row_for_current(self, node_id: str) -> tuple[Any, Any]:
        return self._state_space_model.c_row_current(node_id), self._state_space_model.d_row_current(node_id)

    @property
    def sources(self) -> list[str]:
        return self._state_space_model.sources()

def numeric_state_space_model_constructor(circuit) -> StateSpaceMatrixConstructor:
    network = cc.transform_circuit(circuit, w=0)
    state_space_model = ssm.numeric_state_space_model(
        network=network,
        c_values={C.id : float(C.value['C']) for C in [c for c in circuit.components if c.type == 'capacitor']},
        l_values={L.id : float(L.value['L']) for L in [c for c in circuit.components if c.type == 'inductance']}
    )
    return StateSpaceMatrixConstructor(state_space_model)

def numeric_state_space_model(circuit: cc.Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> NumericStateSpaceModel:
    state_space_model = numeric_state_space_model_constructor(circuit)
    return NumericStateSpaceModel(
        A=np.array(state_space_model.A),
        B=np.array(state_space_model.B),
        C=np.array(state_space_model.C(potential_nodes, voltage_ids, current_ids)),
        D=np.array(state_space_model.D(potential_nodes, voltage_ids, current_ids))
    )

def symbolic_state_space_model_constructor(circuit) -> StateSpaceMatrixConstructor:
    def to_symbolic(id: str, value: str) -> sp.Symbol:
        sym_value = sp.sympify(value)
        if sym_value == sp.nan or id == value:
            return sp.Symbol(id, real=True, positive=True)
        return sym_value
    network = cc.transform_symbolic_circuit(circuit, s=sp.sympify(0))
    state_space_model = ssm.symbolic_state_space_model(
        network=network,
        c_values={C.id : to_symbolic(C.id, C.value['C']) for C in [c for c in circuit.components if c.type == 'capacitor']},
        l_values={L.id : to_symbolic(L.id, L.value['L']) for L in [c for c in circuit.components if c.type == 'inductance']}
    )
    return StateSpaceMatrixConstructor(state_space_model)

def symbolic_state_space_model(circuit: cc.Circuit, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> SymbolicStateSpaceModel:
    state_space_model = symbolic_state_space_model_constructor(circuit)
    return SymbolicStateSpaceModel(
        A=state_space_model.A,
        B=state_space_model.B,
        C=state_space_model.C(potential_nodes, voltage_ids, current_ids),
        D=state_space_model.D(potential_nodes, voltage_ids, current_ids)
    )