from .circuit import Circuit, transform_circuit
from ..Network.NodalAnalysis.state_space_model import BranchValues, create_state_space_input_update_matrix
import numpy as np

class StateSpaceModel:
    def __init__(self, circuit: Circuit):
        self._all_Cs = [c for c in circuit.components if c.type == 'capacitor']
        self._A, self._B = create_state_space_input_update_matrix(
            network=transform_circuit(circuit, w=0),
            Cvalues=[BranchValues(value=float(C.value['C']), node1=C.nodes[0], node2=C.nodes[1]) for C in self._all_Cs]
        )

    @property
    def A(self) -> np.ndarray:
        return self._A

    @property
    def B(self) -> np.ndarray:
        return self._B

    @property
    def state_labels(self) -> list[str]:
        return ['v_'+C.id for C in self._all_Cs]

    @property
    def input_labels(self) -> list[str]:
        return []