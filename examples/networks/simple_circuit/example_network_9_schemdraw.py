from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, CurrentSource, Resistor, Line
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 15, 5, 20, 20
Uq = 120
Iq = 4

with Schematic(unit=5) as d:
    d += CurrentSource(I=Iq, name='Iq').up()
    d += Line().right()
    d += (R2_ := Resistor(R=R2, name='R2').right())
    d += (R3_ := Resistor(R=R3, name='R3').down())
    d += Line().left()
    d += Line().left()
    d += Line().right().at(R3_.end)
    d += Resistor(R=R4, name='R4').up()
    d += VoltageSource(V=Uq, name='Uq', precision=1, reverse=True).left()
    d += Resistor(R=R1, name='R1').down().at(R2_.start)
    schemdraw_network = SchematicDiagramAnalyzer(d)
    schemdraw_solution = SchematicDiagramSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R4', precision=3, reverse=True)