from CircuitCalculator.SimpleCircuit.Elements import Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.Network import SchemdrawNetwork
from CircuitCalculator.EquivalentSources import calculate_total_impedeance
from schemdraw import Drawing

if __name__ == '__main__':
    with Drawing() as d:
        d += LabelNode(id='1', id_loc='S')
        d += Line().up().length(4)
        d += Resistor(R=1, name='R1').right()
        d += Line().up().length(2)
        d += (R4:=Resistor(R=4, name='R4').right())
        d += Resistor(R=5, name='R5').right()
        d += Line().down().length(2)
        d += Line().down().length(2)
        d += (R3:=Resistor(R=3, name='R3').left().length(6))
        d += Line().up().length(2)
        d += Line().at(R3.start).down().length(2)
        d += Line().left().length(4.5)
        d += Resistor(R=2, name='R2').left()
        d += Line().left().length(1.5)
        d += Line().at(R4.end).up().length(2)
        d += Line().right().length(1.5)
        d += Resistor(R=6, name='R6').right()
        d += Line().right().length(1.5)
        d += Line().down().length(4)
        d += LabelNode(id='2', id_loc='S')
        d += Resistor(R=7, name='R7').left()
        schemdraw_network = SchemdrawNetwork(d)

R = calculate_total_impedeance(schemdraw_network.network, '1', '2').real
print(f'{R=}Ohm')