from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.DiagramParser import network_parser
from CircuitCalculator.EquivalentSources import calculate_total_impedeance

if __name__ == '__main__':
    with Schematic(unit=3) as schematic:
        schematic += LabelNode(id='1', id_loc='S')
        schematic += Line().up().length(4)
        schematic += Resistor(R=1, name='R1').right()
        schematic += Line().up().length(2)
        schematic += (R4:=Resistor(R=4, name='R4').right())
        schematic += Resistor(R=5, name='R5').right()
        schematic += Line().down().length(2)
        schematic += Line().down().length(2)
        schematic += (R3:=Resistor(R=3, name='R3').left().length(6))
        schematic += Line().up().length(2)
        schematic += Line().at(R3.start).down().length(2)
        schematic += Line().left().length(4.5)
        schematic += Resistor(R=2, name='R2').left()
        schematic += Line().left().length(1.5)
        schematic += Line().at(R4.end).up().length(2)
        schematic += Line().right().length(1.5)
        schematic += Resistor(R=6, name='R6').right()
        schematic += Line().right().length(1.5)
        schematic += Line().down().length(4)
        schematic += LabelNode(id='2', id_loc='S')
        schematic += Resistor(R=7, name='R7').left()
        R = calculate_total_impedeance(network_parser(schematic), '1', '2').real
        print(f'{R=:4.2f}Ohm')
