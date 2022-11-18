from CircuitCalculator.SimpleCircuit.Schematics import Schematic
from CircuitCalculator.SimpleCircuit.Elements import RealCurrentSource, Resistor, Line, Ground
from CircuitCalculator.SimpleCircuit.NetworkParser import SchemdrawNetwork, SchemdrawSolution
from CircuitCalculator.ClassicNodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as d:
        d += RealCurrentSource(I=1, R=100, name='I1').up()
        d += (R1:=Resistor(R=10, name='R1').right())
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
        schemdraw_network = SchemdrawNetwork(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2', reverse=False)
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('I1', top=True)