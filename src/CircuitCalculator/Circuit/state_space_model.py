from .circuit import Circuit, transform_circuit
import numpy as np
from ..Network.NodalAnalysis.state_space_model import NodalStateSpaceModel, BranchValues, Output, OutputType


class StateSpaceModel:
    def __init__(self, circuit: Circuit):
        self._all_Cs = [c for c in circuit.components if c.type == 'capacitor']
        self._state_space_model = NodalStateSpaceModel(
            network=transform_circuit(circuit, w=0),
            c_values=[BranchValues(value=float(C.value['C']), id=C.id, node1=C.nodes[0], node2=C.nodes[1]) for C in self._all_Cs],
            output_values=[Output(OutputType.POTENTIAL, '1'), Output(OutputType.POTENTIAL, '2'), Output(OutputType.POTENTIAL, '3')]#, Output(OutputType.VOLTAGE, 'R3')]
        )

    @property
    def A(self) -> np.ndarray:
        return self._state_space_model.A

    @property
    def B(self) -> np.ndarray:
        return self._state_space_model.B

    @property
    def C(self) -> np.ndarray:
        return self._state_space_model.C

    @property
    def D(self) -> np.ndarray:
        return self._state_space_model.D

    @property
    def state_labels(self) -> list[str]:
        return self._state_space_model.state_labels

    @property
    def input_labels(self) -> list[str]:
        return self._state_space_model.input_labels