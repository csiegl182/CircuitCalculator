from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, Ground, VoltageSource, RealVoltageSource
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution, network_parser
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as schematic:
        schematic += (U:=RealVoltageSource(
            voltage_source=VoltageSource(V=9, name='Uq'),
            resistor=Resistor(R=1, name='Ri')).up())
        schematic += Line().right()
        schematic += Resistor(R=2, name='R').down()
        schematic += Line().left()
        schematic += Ground()
        solution = nodal_analysis_solver(network_parser(schematic))
        schemdraw_solution = SchematicDiagramSolution(SchematicDiagramAnalyzer(schematic), solution)
        schematic += schemdraw_solution.draw_voltage('R')
        schematic += schemdraw_solution.draw_current('R')
