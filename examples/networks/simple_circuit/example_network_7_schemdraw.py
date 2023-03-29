from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution, network_parser
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 10, 20, 30, 40
Uq1, Uq2, Uq3, Iq4 = 1, 2, 3, 0.1

with Schematic(unit=5) as schematic:
    schematic += VoltageSource(V=Uq1, name='Uq1', precision=1).up()
    schematic += LabelNode(id='1', id_loc='W')
    schematic += VoltageSource(V=Uq2, name='Uq2', precision=1).up()
    schematic += (_R1:=Resistor(R=R1, name='R1').right())
    schematic += Line().down()
    schematic += Line().down()
    schematic += Line().left()
    solution = nodal_analysis_solver(network_parser(schematic))
    schemdraw_solution = SchematicDiagramSolution(SchematicDiagramAnalyzer(schematic), solution)
    schematic += schemdraw_solution.draw_voltage('R1')
    schematic += schemdraw_solution.draw_current('R1')