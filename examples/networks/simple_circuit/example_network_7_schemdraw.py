from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 10, 20, 30, 40
Uq1, Uq2, Uq3, Iq4 = 1, 2, 3, 0.1

with Schematic(unit=5) as d:
    d += VoltageSource(V=Uq1, name='Uq1', precision=1).up()
    d += LabelNode(id='1', id_loc='W')
    d += VoltageSource(V=Uq2, name='Uq2', precision=1).up()
    d += (_R1:=Resistor(R=R1, name='R1').right())
    d += Line().down()
    d += Line().down()
    d += Line().left()
    schemdraw_network = SchematicDiagramAnalyzer(d)
    schemdraw_solution = SchematicDiagramSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R1')
    d += schemdraw_solution.draw_current('R1', ofst=1.2)