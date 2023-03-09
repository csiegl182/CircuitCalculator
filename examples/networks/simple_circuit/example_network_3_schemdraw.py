from CircuitCalculator.SimpleCircuit.Elements import Schematic, VoltageSource, Resistor, Line, Ground
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as d:
        d += (U1:=VoltageSource(V=1, R=0, name='U1').up())
        d += (R1:=Resistor(R=10, name='R1').right())
        d += (R2:=Resistor(R=20, name='R2').down())
        d += Line().left()
        d += (R3:=Resistor(R=30, name='R3').at(R1.end).right())
        d += (R4:=Resistor(R=40, name='R4').down())
        d += (R5:=Resistor(R=50, name='R5').left())
        d += Line().at(R4.end).down()
        d += (U2:=VoltageSource(V=2, R=0, name='U2').left())
        d += Line().left()
        d += Ground()
        d += Line().up()
        schemdraw_network = SchematicDiagramAnalyzer(d)
        schemdraw_solution = SchematicDiagramSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2')
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_current('U2')
        d += schemdraw_solution.draw_current('R4')
        d += schemdraw_solution.draw_current('R5')