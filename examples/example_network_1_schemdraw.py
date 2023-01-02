from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, Ground, CurrentSource, RealCurrentSource
from CircuitCalculator.SimpleCircuit.NetworkParser import NetworkDiagramParser, SchemdrawSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as d:
        d += (I:=RealCurrentSource(
            current_source=CurrentSource(I=1, R=100, name='Ix'),
            resistor=Resistor(R=100, name='Ri'), d='up'))
        d += Line().right()
        d += (R1:=Resistor(R=10, name='R1')).right()
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
        d += Line().left()
        schemdraw_network = NetworkDiagramParser(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2', reverse=False)
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('I1', top=True)
