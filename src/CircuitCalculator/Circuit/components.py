from dataclasses import dataclass, field
from abc import ABC
    
@dataclass(frozen=True)
class Component(ABC):
    nodes : tuple[str]
    type : str
    id : str
    is_active: bool = field(default=False, init=False)
    w: float = field(default=0, init=False)

@dataclass(frozen=True)
class TwoPoleComponent(Component):
    nodes : tuple[str, str]

@dataclass(frozen=True)
class Resistor(TwoPoleComponent):
    R : float
    type : str = field(default='resistor', init=False)

@dataclass(frozen=True)
class Capacitor(TwoPoleComponent):
    C : float
    type : str = field(default='capacitor', init=False)

@dataclass(frozen=True)
class Inductance(TwoPoleComponent):
    L : float
    type : str = field(default='inductance', init=False)

@dataclass(frozen=True)
class Source(TwoPoleComponent):
    is_active : bool = field(default=True, init=False)
    w : float = field(default=0.0)
    phi : float = field(default=0.0)

@dataclass(frozen=True)
class CurrentSource(Source):
    I : float = field(default=0.0)
    type : str = field(default='current_source', init=False)

@dataclass(frozen=True)
class VoltageSource(Source):
    V : float = field(default=0.0)
    type : str = field(default='voltage_source', init=False)

@dataclass(frozen=True)
class LinearCurrentSource(CurrentSource):
    G : float = field(default=0.0)
    type : str = field(default='linear_current_source', init=False)

@dataclass(frozen=True)
class LinearVoltageSource(VoltageSource):
    R : float = field(default=0.0)
    type : str = field(default='linear_voltage_source', init=False)

@dataclass(frozen=True)
class Ground(Component):
    id : str = field(default='gnd')
    type : str = field(default='ground', init=False)
    nodes : tuple[str]