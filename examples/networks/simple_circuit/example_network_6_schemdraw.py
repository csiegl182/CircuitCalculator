from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, network_parser
from CircuitCalculator.EquivalentSources import calculate_total_impedeance

if __name__ == '__main__':
    with Schematic() as schem:
        schem += LabelNode(id='1', id_loc='S')
        schem += Line().up().length(4)
        schem += Resistor(R=1, name='R1').right()
        schem += Line().up().length(2)
        schem += (R4:=Resistor(R=4, name='R4').right())
        schem += Resistor(R=5, name='R5').right()
        schem += Line().down().length(2)
        schem += Line().down().length(2)
        schem += (R3:=Resistor(R=3, name='R3').left().length(6))
        schem += Line().up().length(2)
        schem += Line().at(R3.start).down().length(2)
        schem += Line().left().length(4.5)
        schem += Resistor(R=2, name='R2').left()
        schem += Line().left().length(1.5)
        schem += Line().at(R4.end).up().length(2)
        schem += Line().right().length(1.5)
        schem += Resistor(R=6, name='R6').right()
        schem += Line().right().length(1.5)
        schem += Line().down().length(4)
        schem += LabelNode(id='2', id_loc='S')
        schem += Resistor(R=7, name='R7').left()
        R = calculate_total_impedeance(network_parser(schem), '1', '2').real
        print(f'{R=:4.2f}Ohm')
