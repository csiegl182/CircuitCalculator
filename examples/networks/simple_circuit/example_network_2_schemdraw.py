from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, Resistor, Line, Ground
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as d:
        d += (U1:=VoltageSource(V=1, R=0, name='U1').up())
        d += Line().right()
        d += (R1:=Resistor(R=10, name='R1').down())
        d += Line().left()
        d += Ground()
        d += Resistor(R=20, name='R2').at(R1.start).right()
        d += Resistor(R=30, name='R3').down()
        d += Line().left()
        schemdraw_network = SchematicDiagramAnalyzer(d)
        schemdraw_solution = SchematicDiagramSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2')
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('R3')
        d += schemdraw_solution.draw_current('R3', start=False)
        d += schemdraw_solution.draw_current('U1')