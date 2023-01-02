from CircuitCalculator.SimpleCircuit.Elements import Schematic, Resistor, Line, Ground, VoltageSource, RealVoltageSource
from CircuitCalculator.SimpleCircuit.NetworkParser import NetworkDiagramParser, SchemdrawSolution
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    with Schematic() as d:
        d += (U:=RealVoltageSource(
            voltage_source=VoltageSource(V=9, name='Uq', d='up'),
            resistor=Resistor(R=1, name='Ri', d='right')))
        d += Line().right()
        d += Resistor(R=2, name='R').down()
        d += Line().left()
        d += Line().left()
        d += Ground()
        schemdraw_network = NetworkDiagramParser(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R')
        d += schemdraw_solution.draw_current('R')
