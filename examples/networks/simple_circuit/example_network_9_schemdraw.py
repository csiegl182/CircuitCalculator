from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, CurrentSource, Resistor, Line
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution, network_parser
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 15, 5, 20, 20
Uq = 120
Iq = 4

with Schematic(unit=5) as schematic:
    schematic += CurrentSource(I=Iq, name='Iq').up()
    schematic += Line().right()
    schematic += (R2_ := Resistor(R=R2, name='R2').right())
    schematic += (R3_ := Resistor(R=R3, name='R3').down())
    schematic += Line().left()
    schematic += Line().left()
    schematic += Line().right().at(R3_.end)
    schematic += Resistor(R=R4, name='R4').up()
    schematic += VoltageSource(V=Uq, name='Uq', precision=3, reverse=True).left()
    schematic += Resistor(R=R1, name='R1').down().at(R2_.start)
    solution = nodal_analysis_solver(network_parser(schematic))
    schemdraw_solution = SchematicDiagramSolution(SchematicDiagramAnalyzer(schematic), solution)
    schematic += schemdraw_solution.draw_voltage('R4', precision=3, reverse=True)