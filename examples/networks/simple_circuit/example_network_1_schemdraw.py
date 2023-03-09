from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, Ground, CurrentSource, RealCurrentSource
from CircuitCalculator.SimpleCircuit.DiagramParser import SchematicDiagramAnalyzer, SchematicDiagramSolution, network_parser
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as schematic:
        schematic += (I:=RealCurrentSource(
            current_source=CurrentSource(I=1, R=100, name='Ix'),
            resistor=Resistor(R=100, name='Ri'), d='up'))
        schematic += Line().right()
        schematic += (R1:=Resistor(R=10, name='R1')).right()
        schematic += Resistor(R=20, name='R2').down()
        schematic += Line().left()
        schematic += Ground()
        schematic += Line().left()
        solution = nodal_analysis_solver(network_parser(schematic))
        schemdraw_solution = SchematicDiagramSolution(SchematicDiagramAnalyzer(schematic), solution)
        schematic += schemdraw_solution.draw_voltage('R1')
        schematic += schemdraw_solution.draw_current('R1')
        schematic += schemdraw_solution.draw_voltage('R2', reverse=False)
        schematic += schemdraw_solution.draw_current('R2')
        schematic += schemdraw_solution.draw_voltage('Ix', top=True)
